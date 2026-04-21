"""Background enrichment task for learning map nodes.

When a curriculum is created, approved, or mapped, this task
enriches every node with teaching guidance, practice items,
and assessment criteria so content is ready before the child
starts their first activity.
"""

import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)


def enrich_learning_map_sync(learning_map_id: str, household_id: str) -> dict:
    """Synchronous wrapper for the async enrichment pipeline."""
    return asyncio.run(_enrich_map(uuid.UUID(learning_map_id), uuid.UUID(household_id)))


async def _enrich_map(learning_map_id: uuid.UUID, household_id: uuid.UUID) -> dict:
    """Enrich all unenriched nodes in a learning map."""
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from app.core.config import settings
    from app.core.database import set_tenant
    from app.models.curriculum import LearningMap, LearningNode

    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as db:
        await set_tenant(db, household_id)
        # Get the map
        map_result = await db.execute(
            select(LearningMap).where(
                LearningMap.id == learning_map_id,
                LearningMap.household_id == household_id,
            )
        )
        learning_map = map_result.scalar_one_or_none()
        if not learning_map:
            logger.warning(f"Learning map {learning_map_id} not found for enrichment")
            await engine.dispose()
            return {"enriched": 0, "failed": 0, "skipped": 0}

        # Get all nodes
        node_result = await db.execute(
            select(LearningNode).where(
                LearningNode.learning_map_id == learning_map_id,
            )
        )
        all_nodes = node_result.scalars().all()
        total = len(all_nodes)

        enriched = 0
        failed = 0
        skipped = 0

        for i, node in enumerate(all_nodes):
            # Skip already enriched nodes
            if node.content and isinstance(node.content, dict) and node.content.get("enriched"):
                skipped += 1
                continue

            try:
                # Try seed content first
                seed = _get_seed_content(node.title)
                if seed:
                    node.content = seed
                    enriched += 1
                    logger.info(f"Seed content applied to node '{node.title}' ({i + 1}/{total})")
                else:
                    # Mark as needing AI enrichment and inject scope metadata
                    if not node.content:
                        node.content = {}
                    node.content["needs_enrichment"] = True
                    scope_meta = _get_scope_metadata(node.title)
                    if scope_meta:
                        node.content["scope_metadata"] = scope_meta
                        logger.info(f"Scope metadata injected for '{node.title}' ({i + 1}/{total})")
                    enriched += 1
                    logger.info(f"Marked node '{node.title}' for enrichment ({i + 1}/{total})")
            except Exception as e:
                failed += 1
                logger.warning(f"Failed to enrich node '{node.title}': {e}")

        await db.commit()

    await engine.dispose()

    result = {"enriched": enriched, "failed": failed, "skipped": skipped, "total": total}
    logger.info(f"Enrichment complete for map {learning_map_id}: {result}")
    return result


def _get_seed_content(node_title: str) -> dict | None:
    """Check if pre-written seed content exists for this topic."""
    try:
        from app.content.seed_content import SEED_CONTENT

        title_lower = node_title.lower().strip()
        for key, content in SEED_CONTENT.items():
            if key.lower() in title_lower or title_lower in key.lower():
                return content
        return None
    except ImportError:
        return None


def _get_scope_metadata(node_title: str, subject_name: str | None = None) -> dict | None:
    """Look up scope sequence metadata for a node by title match.

    Returns key_concepts, assessment_indicators, and alignment data
    that can be injected into content or passed to the content architect.
    """
    try:
        from app.content.scope_sequences import SCOPE_SEQUENCES
        from app.core.learning_levels import SUBJECT_CATALOG

        title_lower = node_title.lower().strip()

        # Determine which subjects to search
        search_subjects = list(SCOPE_SEQUENCES.keys())
        if subject_name:
            subj_id = subject_name.lower().replace(" ", "_").replace("&", "and")
            for cat in SUBJECT_CATALOG.values():
                for s in cat:
                    if s["name"].lower() == subject_name.lower() or s["id"] == subj_id:
                        subj_id = s["id"]
                        break
            if subj_id in SCOPE_SEQUENCES:
                search_subjects = [subj_id]

        for subj in search_subjects:
            for _level_name, topics in SCOPE_SEQUENCES[subj].items():
                for topic in topics:
                    if topic["title"].lower().strip() == title_lower:
                        return {
                            "scope_ref": topic["ref"],
                            "key_concepts": topic.get("key_concepts", []),
                            "assessment_indicators": topic.get("assessment_indicators", []),
                            "classical_alignment": topic.get("classical_alignment", ""),
                            "charlotte_mason_alignment": topic.get("charlotte_mason_alignment", ""),
                            "standard_alignment": topic.get("standard_alignment", ""),
                            "estimated_weeks": topic.get("estimated_weeks", 1),
                        }
        return None
    except Exception:
        return None
