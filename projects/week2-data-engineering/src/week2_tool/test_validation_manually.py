"""
A batch of orders with SEVERAL deliberate problems, to prove
validate_rows() catches each one correctly, with the right reason.
"""
from validate import validate_rows

test_batch = [
    # Row 1: completely valid — should pass
    {"order_id": 1, "customer_email": "nelly@example.com", "price": 25.50, "quantity": 2, "category": "electronics"},

    # Row 2: negative price — should fail the price > 0 rule
    {"order_id": 2, "customer_email": "bad@example.com", "price": -5.00, "quantity": 1, "category": "food"},

    # Row 3: invalid email — missing '@', should fail our custom validator
    {"order_id": 3, "customer_email": "not-an-email", "price": 10.00, "quantity": 1, "category": "books"},

    # Row 4: invalid category — not in our allowed list
    {"order_id": 4, "customer_email": "ok@example.com", "price": 15.00, "quantity": 1, "category": "furniture"},

    # Row 5: missing required field entirely (no order_id)
    {"customer_email": "missing@example.com", "price": 5.00, "quantity": 1, "category": "food"},

    # Row 6: quantity is 0 — fails the "at least 1" rule
    {"order_id": 6, "customer_email": "zero@example.com", "price": 8.00, "quantity": 0, "category": "clothing"},
]

valid, invalid = validate_rows(test_batch)

print(f"\n--- RESULTS ---")
print(f"Valid rows: {len(valid)}")
print(f"Invalid rows: {len(invalid)}")

print(f"\n--- VALID ---")
for order in valid:
    print(order)

print(f"\n--- INVALID (with reasons) ---")
for item in invalid:
    print(f"Row: {item['row']}")
    for err in item["errors"]:
        print(f"  -> {err['msg']}")
