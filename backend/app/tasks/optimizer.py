"""FSRS per-child weight optimizer (Section 5.3).

Runs weekly. For each child with >= 50 new reviews since last optimization,
runs the py-fsrs Optimizer to compute personalized 21-parameter weights
from the child's actual review history.
"""

import asyncio
import time
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.models.identity import Child
from app.models.state import FSRSCard, ReviewLog

import structlog

logger = structlog.get_logger()

MIN_REVIEWS_FIRST = 100
MIN_REVIEWS_INCREMENTAL = 50


def _build_fsrs_review_logs(
    db_reviews: list[ReviewLog],
    db_cards: dict,
) -> list:
    """Convert DB ReviewLog entries to py-fsrs ReviewLog objects.

    The py-fsrs Optimizer expects ReviewLog objects with:
    - card_id: int (groups reviews by card)
    - rating: Rating enum
    - review_datetime: datetime
    - review_duration: int | None
    """
    from fsrs import Rating as FSRSRating
    from fsrs.review_log import ReviewLog as FSRSReviewLog

    rating_map = {
        1: FSRSRating.Again,
        2: FSRSRating.Hard,
        3: FSRSRating.Good,
        4: FSRSRating.Easy,
    }

    # We need stable integer card IDs for the optimizer (it groups by card_id).
    # Map UUID card_ids to sequential integers.
    card_uuid_to_int: dict[str, int] = {}
    next_id = 1

    fsrs_logs = []
    for review in db_reviews:
        card_key = str(review.card_id)
        if card_key not in card_uuid_to_int:
            card_uuid_to_int[card_key] = next_id
            next_id += 1

        int_card_id = card_uuid_to_int[card_key]

        # Map the DB rating (stored as int 1-4) to FSRS Rating
        rating_val = review.rating
        if hasattr(rating_val, 'value'):
            rating_val = rating_val.value
        rating_val = int(rating_val)
        fsrs_rating = rating_map.get(rating_val, FSRSRating.Good)

        # Use reviewed_at for the review timestamp, fall back to created_at
        review_dt = review.reviewed_at or review.created_at
        if review_dt and review_dt.tzinfo is None:
            from datetime import timezone
            review_dt = review_dt.replace(tzinfo=timezone.utc)

        duration_ms = review.review_duration_ms

        fsrs_logs.append(FSRSReviewLog(
            card_id=int_card_id,
            rating=fsrs_rating,
            review_datetime=review_dt,
            review_duration=duration_ms,
        ))

    return fsrs_logs


async def optimize_fsrs_weights(
    session_factory: async_sessionmaker | None = None,
) -> dict:
    """Run FSRS weight optimization for eligible children."""
    start = time.monotonic()

    if session_factory is None:
        engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    children_optimized = 0
    children_skipped = 0

    async with session_factory() as db:
        # Get all active children
        children_result = await db.execute(
            select(Child).where(Child.is_active == True)  # noqa: E712
        )
        children = children_result.scalars().all()

        for child in children:
            # Count total reviews
            count_result = await db.execute(
                select(func.count(ReviewLog.id)).where(
                    ReviewLog.child_id == child.id
                )
            )
            total_reviews = count_result.scalar() or 0

            # Determine threshold
            has_weights = child.fsrs_weights is not None
            threshold = MIN_REVIEWS_INCREMENTAL if has_weights else MIN_REVIEWS_FIRST

            if total_reviews < threshold:
                children_skipped += 1
                continue

            try:
                previous_weights = child.fsrs_weights

                # Fetch all review logs for this child
                reviews_result = await db.execute(
                    select(ReviewLog).where(
                        ReviewLog.child_id == child.id
                    ).order_by(ReviewLog.created_at.asc())
                )
                reviews = reviews_result.scalars().all()

                # Fetch card info for mapping
                card_ids = list({r.card_id for r in reviews})
                cards_result = await db.execute(
                    select(FSRSCard).where(FSRSCard.id.in_(card_ids))
                ) if card_ids else None
                cards = {c.id: c for c in (cards_result.scalars().all() if cards_result else [])}

                # Convert to py-fsrs ReviewLog format
                fsrs_logs = _build_fsrs_review_logs(reviews, cards)

                if len(fsrs_logs) < threshold:
                    children_skipped += 1
                    continue

                # Run the py-fsrs Optimizer
                from fsrs.optimizer import Optimizer
                optimizer = Optimizer(fsrs_logs)
                new_weights = optimizer.compute_optimal_parameters()

                child.fsrs_weights = new_weights
                children_optimized += 1

                logger.info(
                    "fsrs_optimized",
                    child_id=str(child.id),
                    reviews_used=total_reviews,
                    previous_weights=str(previous_weights[:5]) if previous_weights else "none",
                    new_weights=str(new_weights[:5]) if new_weights else "none",
                )

            except Exception as e:
                logger.error("fsrs_optimization_failed", child_id=str(child.id), error=str(e))
                children_skipped += 1

        await db.commit()

    elapsed_ms = int((time.monotonic() - start) * 1000)
    return {
        "children_optimized": children_optimized,
        "children_skipped": children_skipped,
        "duration_ms": elapsed_ms,
    }


def run_optimizer_sync() -> dict:
    return asyncio.run(optimize_fsrs_weights())
