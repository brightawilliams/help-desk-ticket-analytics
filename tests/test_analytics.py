import sqlite3
import tempfile
import unittest
from pathlib import Path

from helpdesk_analytics import build_database, load_named_queries, run_analysis
from helpdesk_analytics.reporting import build_report


ROOT = Path(__file__).resolve().parents[1]
AS_OF = "2026-08-31T23:59:59"


class HelpDeskAnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.connection = build_database(
            ROOT / "sql" / "schema.sql",
            ROOT / "data" / "technicians.csv",
            ROOT / "data" / "tickets.csv",
        )
        self.queries = load_named_queries(ROOT / "sql" / "analysis_queries.sql")
        self.results = run_analysis(self.connection, self.queries, as_of=AS_OF)

    def tearDown(self):
        self.connection.close()

    def test_sample_data_counts_are_stable(self):
        summary = self.results["executive_summary"][0]
        self.assertEqual(summary["total_tickets"], 24)
        self.assertEqual(summary["completed_tickets"], 20)
        self.assertEqual(summary["open_backlog"], 4)

    def test_all_expected_queries_are_loaded(self):
        self.assertEqual(
            set(self.queries),
            {
                "executive_summary",
                "category_performance",
                "priority_sla",
                "technician_performance",
                "channel_volume",
                "open_backlog",
            },
        )

    def test_backlog_is_ordered_by_priority(self):
        priorities = [row["priority"] for row in self.results["open_backlog"]]
        self.assertEqual(priorities, ["Critical", "High", "Medium", "Low"])

    def test_foreign_key_rejects_unknown_technician(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO tickets VALUES (
                    'BAD-1', '2026-08-31T10:00:00', NULL, 'Open', 'Low',
                    'Other', 'Portal', 'Finance', 'UNKNOWN', 5, NULL, 0
                )
                """
            )

    def test_report_contains_key_sections(self):
        report = build_report(self.results, as_of=AS_OF)
        self.assertIn("Total tickets: 24", report)
        self.assertIn("## First-response SLA by priority", report)
        self.assertIn("## Open backlog", report)

    def test_empty_query_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.sql"
            path.write_text("SELECT 1;", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "No named SQL queries"):
                load_named_queries(path)


if __name__ == "__main__":
    unittest.main()
