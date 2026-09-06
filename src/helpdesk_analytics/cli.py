"""Command-line entry point for the help-desk analytics report."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .analytics import load_named_queries, run_analysis
from .database import build_database
from .reporting import build_report


DEFAULT_AS_OF = "2026-08-31T23:59:59"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze fictional help-desk tickets with SQLite and Python."
    )
    parser.add_argument("--as-of", default=DEFAULT_AS_OF, help="ISO timestamp for backlog age")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("helpdesk_report.md"),
        help="Markdown report path",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = _project_root()
    try:
        connection = build_database(
            root / "sql" / "schema.sql",
            root / "data" / "technicians.csv",
            root / "data" / "tickets.csv",
        )
        queries = load_named_queries(root / "sql" / "analysis_queries.sql")
        results = run_analysis(connection, queries, as_of=args.as_of)
        args.output.write_text(build_report(results, as_of=args.as_of), encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    finally:
        if "connection" in locals():
            connection.close()

    print(f"Analyzed {results['executive_summary'][0]['total_tickets']} tickets.")
    print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

