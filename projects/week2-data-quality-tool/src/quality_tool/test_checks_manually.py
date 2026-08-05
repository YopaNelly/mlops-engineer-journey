"""
Runs each check independently against the deliberately broken sample CSV,
proving each function catches exactly the problems we put there on purpose.
"""
import pandas as pd
from checks import check_missing, check_types, check_ranges

df = pd.read_csv("../../sample_broken_data.csv")

print("--- check_missing ---")
print(check_missing(df, required_columns=["id", "price", "age", "category"]))

print("\n--- check_types ---")
print(check_types(df, expected_types={"price": float, "age": int}))

print("\n--- check_ranges ---")
print(check_ranges(df, ranges={"age": (0, 120), "price": (0, 10000)}))
