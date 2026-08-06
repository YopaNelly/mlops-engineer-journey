import pandas as pd
from .report import run_quality_checks
from .save_report import save_json_report
from .render_html import render_html_report

df = pd.read_csv("sample_broken_data.csv")

report = run_quality_checks(
    df,
    required_columns=["id", "price", "age", "category"],
    expected_types={"price": float, "age": int},
    ranges={"age": (0, 120), "price": (0, 10000)},
)

print(report)

save_json_report(report, "quality_report.json")
render_html_report(report, "quality_report.html")

print("\nSaved quality_report.json and quality_report.html")
