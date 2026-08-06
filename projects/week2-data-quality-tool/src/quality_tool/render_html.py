from jinja2 import Environment, FileSystemLoader


def render_html_report(report: dict, output_path: str = "quality_report.html") -> None:
    # Tell Jinja2 where to find template files (the "templates" folder)
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    # This fills in every {{ }} placeholder in the template with real data
    html_content = template.render(report=report)

    with open(output_path, "w") as f:
        f.write(html_content)
