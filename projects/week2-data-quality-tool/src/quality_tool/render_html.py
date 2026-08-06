from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def render_html_report(report: dict, output_path: str = "quality_report.html") -> None:
    # Find the templates/ folder RELATIVE TO THIS FILE, not relative to
    # wherever the script happens to be run from. This is the fix —
    # Path(__file__) always points to render_html.py's own location,
    # no matter what folder you were sitting in when you ran the command.
    this_file = Path(__file__).resolve()
    project_root = this_file.parent.parent.parent  # up from quality_tool/ -> src/ -> project root
    templates_dir = project_root / "templates"

    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("report.html")

    html_content = template.render(report=report)

    with open(output_path, "w") as f:
        f.write(html_content)
