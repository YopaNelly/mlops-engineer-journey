"""
Takes a batch of raw dictionaries (like rows from a CSV) and splits them
into two lists: ones that passed validation, and ones that didn't —
WITH the specific reason each invalid row failed, logged clearly.

This is the core principle from earlier in the week, repeated here:
never let one bad row silently corrupt or get lost in a whole batch.
"""

from pydantic import ValidationError
from .schemas import Order
from logging import getLogger, basicConfig, INFO

basicConfig(level=INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = getLogger(__name__)


def validate_rows(raw_rows: list[dict]) -> tuple[list[Order], list[dict]]:
    """
    raw_rows: a list of plain dictionaries, e.g. [{"order_id": 1, "price": 9.99, ...}, ...]

    Returns TWO lists:
      valid   -> a list of proper Order objects, guaranteed to follow every rule
      invalid -> a list of dicts, each with the original row PLUS the reason it failed
    """
    valid: list[Order] = []
    invalid: list[dict] = []

    for row in raw_rows:
        try:
            # This is the actual validation step. Order(**row) tries to build
            # a real Order object out of the raw dict. If ANY rule is broken,
            # pydantic raises a ValidationError here instead of returning
            # something silently wrong.
            order = Order(**row)
            valid.append(order)

        except ValidationError as e:
            # e.errors() gives a structured, detailed breakdown of exactly
            # what went wrong — which field, and why. We keep the original
            # row AND that reason together, so nothing about the failure is lost.
            invalid.append({
                "row": row,
                "errors": e.errors()
            })
            logger.warning(f"Row rejected: {row} — reason: {e.errors()}")

    logger.info(f"Validation complete: {len(valid)} valid, {len(invalid)} invalid")
    return valid, invalid
