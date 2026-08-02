"""
Proves extract, transform, and load can each be tested completely
independently — no need to run the whole pipeline to test one piece.
"""
import pandas as pd
import sys
sys.path.insert(0, "src")

from my_tool.etl import transform


def test_transform_removes_missing_and_duplicates():
    # Testing transform() needs ONLY a dataframe — no file, no database
    raw = pd.DataFrame({
        "id": [1, 2, 2, 3],
        "price": ["$5.00", "$6.00", "$6.00", None],
        "category": ["a", "b", "b", "c"],
    })

    result = transform(raw, required_columns=["id", "price", "category"], numeric_columns=["price"])

    # Row 3 had a missing price -> dropped
    # Row 2 was duplicated -> deduped
    assert len(result) == 2
    assert result["price"].tolist() == [5.0, 6.0]
