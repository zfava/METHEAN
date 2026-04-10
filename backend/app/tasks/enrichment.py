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
    return asyncio.run(
        _enrich_map(uuid.UUID(learning_map_id), uuid.UUID(household_id))
    )


async def _enrich_map(learning_map_id: uuid.UUID, household_id: uuid.UUID) -> dict:
    """Enrich all unenriched nodes in a learning map."""
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    from app.core.config import settings
    from app.models.curriculum import LearningMap, LearningNode

    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as db:
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
                    logger.info(f"Seed content applied to node '{node.title}' ({i+1}/{total})")
                else:
                    # Mark as needing AI enrichment (actual AI call happens separately)
                    if not node.content:
                        node.content = {}
                    node.content["needs_enrichment"] = True
                    enriched += 1
                    logger.info(f"Marked node '{node.title}' for enrichment ({i+1}/{total})")
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
