"""Graph state channels for the record-repair pipeline.

The workers run in parallel (one per violation) and each writes its fix to the
shared `record` channel in the same superstep, so `record` needs a reducer that
merges concurrent field updates rather than letting one write clobber the others.
"""

from __future__ import annotations

from typing import Annotated, Any, TypedDict


def merge_fields(existing: dict, update: dict) -> dict:
    """Field-level merge so concurrent worker writes accumulate."""
    merged = dict(existing)
    merged.update(update)
    return merged


class RepairState(TypedDict, total=False):
    record: Annotated[dict[str, Any], merge_fields]
    verdict: str  # "approve" | "revise"; last write wins
