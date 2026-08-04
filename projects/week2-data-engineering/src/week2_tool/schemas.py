"""
This file defines what a VALID row of data looks like, using pydantic.
We're modeling a simple e-commerce order — think of it as the form
every incoming order must fill out correctly before we trust it.
"""

from pydantic import BaseModel, Field, field_validator


class Order(BaseModel):
    """
    Each attribute below is one 'box on the form', with its own rule.
    """

    # order_id must be a whole number. No default given, so it's REQUIRED —
    # pydantic will reject any row missing this field entirely.
    order_id: int

    # customer_email must be a string. We'll add a real format check below.
    customer_email: str

    # price must be a float, and Field(gt=0) means "greater than 0" —
    # a price of 0 or negative is rejected automatically, no extra code needed.
    price: float = Field(gt=0, description="Order price, must be positive")

    # quantity must be a whole number, at least 1 — you can't order zero items.
    quantity: int = Field(ge=1, description="Must order at least 1 item")

    # category must be one of a fixed, known set of values — anything else
    # is almost certainly a typo or bad data, not a real new category.
    category: str = Field(pattern="^(electronics|clothing|food|books)$")

    # This is a CUSTOM rule pydantic can't express with Field() alone —
    # a real, deliberate check that customer_email actually looks like an email.
    @field_validator("customer_email")
    @classmethod
    def email_must_contain_at_symbol(cls, value: str) -> str:
        if "@" not in value:
            # Raising ValueError here is how you tell pydantic
            # "this value is not acceptable" — it becomes part of the
            # validation error pydantic reports back automatically.
            raise ValueError(f"'{value}' is not a valid email — missing '@'")
        return value
