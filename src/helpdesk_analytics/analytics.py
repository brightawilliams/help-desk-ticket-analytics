"""Load named SQL statements and run the help-desk analysis."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any


QUERY_MARKER = re.compile(r"^-- name: ([a-z][a-z0-9_]*)\s*$", re.MULTILINE)


def load_named_queries(path: Path) -> dict[str, str]:
    """Parse SQL blocks introduced by ``-- name: query_name`` comments."""
    source = path.read_text(encoding="utf-8")
    matches = list(QUERY_MARKER.finditer(source))
    if not matches:
        raise ValueError("No named SQL queries were found")

    queries: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        statement = source[start:end].strip()
        if not statement:
            raise ValueError(f"Query '{match.group(1)}' is empty")
        queries[match.group(1)] = statement
    return queries


def run_analysis(
    connection: sqlite3.Connection,
    queries: dict[str, str],
    *,
    as_of: str,
) -> dict[str, list[dict[str, Any]]]:
    """Execute every named query and return JSON-friendly row dictionaries."""
    results: dict[str, list[dict[str, Any]]] = {}
    for name, statement in queries.items():
        rows = connection.execute(statement, {"as_of": as_of}).fetchall()
        results[name] = [dict(row) for row in rows]
    return results

