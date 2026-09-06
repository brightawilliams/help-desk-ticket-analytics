"""Create and populate the SQLite database from versioned CSV files."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_database(schema_path: Path, technicians_path: Path, tickets_path: Path) -> sqlite3.Connection:
    """Return an in-memory database populated with validated portfolio data."""
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(schema_path.read_text(encoding="utf-8"))

    technicians = _read_csv(technicians_path)
    connection.executemany(
        "INSERT INTO technicians (technician_id, name, team) VALUES (:technician_id, :name, :team)",
        technicians,
    )

    tickets = _read_csv(tickets_path)
    normalized = []
    for ticket in tickets:
        item = dict(ticket)
        item["resolved_at"] = item["resolved_at"] or None
        item["first_response_minutes"] = int(item["first_response_minutes"])
        item["satisfaction_score"] = (
            int(item["satisfaction_score"]) if item["satisfaction_score"] else None
        )
        item["reopened"] = int(item["reopened"])
        normalized.append(item)

    connection.executemany(
        """
        INSERT INTO tickets (
            ticket_id, opened_at, resolved_at, status, priority, category,
            channel, department, technician_id, first_response_minutes,
            satisfaction_score, reopened
        ) VALUES (
            :ticket_id, :opened_at, :resolved_at, :status, :priority, :category,
            :channel, :department, :technician_id, :first_response_minutes,
            :satisfaction_score, :reopened
        )
        """,
        normalized,
    )
    connection.commit()
    return connection

