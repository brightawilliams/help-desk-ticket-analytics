"""Render help-desk analytics as a readable Markdown report."""

from __future__ import annotations

from typing import Any, Iterable


SECTION_TITLES = {
    "category_performance": "Category performance",
    "priority_sla": "First-response SLA by priority",
    "technician_performance": "Technician performance",
    "channel_volume": "Ticket volume by channel",
    "open_backlog": "Open backlog",
}


def _label(name: str) -> str:
    return name.replace("_", " ").title()


def _table(rows: Iterable[dict[str, Any]]) -> list[str]:
    items = list(rows)
    if not items:
        return ["No records."]
    columns = list(items[0])
    lines = [
        "| " + " | ".join(_label(column) for column in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in items:
        values = ["—" if row[column] is None else str(row[column]) for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def build_report(results: dict[str, list[dict[str, Any]]], *, as_of: str) -> str:
    """Build a concise report from the required analytics result sets."""
    summary_rows = results.get("executive_summary", [])
    if len(summary_rows) != 1:
        raise ValueError("Executive summary must return exactly one row")
    summary = summary_rows[0]

    lines = [
        "# Help Desk Ticket Analytics Report",
        "",
        f"**Analysis date:** {as_of}",
        "",
        "## Executive summary",
        "",
        f"- Total tickets: {summary['total_tickets']}",
        f"- Completed tickets: {summary['completed_tickets']}",
        f"- Open backlog: {summary['open_backlog']}",
        f"- Average resolution time: {summary['avg_resolution_hours']} hours",
        f"- First-response SLA compliance: {summary['first_response_sla_pct']}%",
        f"- Average satisfaction: {summary['avg_satisfaction']}/5",
    ]

    for key, title in SECTION_TITLES.items():
        if key not in results:
            raise ValueError(f"Missing analysis result: {key}")
        lines.extend(["", f"## {title}", "", *_table(results[key])])

    lines.extend(
        [
            "",
            "## Interpretation notes",
            "",
            "- SLA compliance compares each first response with the target for its priority.",
            "- Resolution time includes resolved and closed tickets only.",
            "- Satisfaction averages exclude tickets without a survey response.",
            "- This fictional dataset is intended for portfolio demonstration only.",
            "",
        ]
    )
    return "\n".join(lines)

