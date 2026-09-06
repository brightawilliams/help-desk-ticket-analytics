# Help Desk Ticket Analytics

A reproducible SQL and Python project that turns help-desk ticket records into
operational metrics for a support team. It loads CSV data into SQLite, runs
clearly named SQL queries, and generates a management-ready Markdown report.

## What this project demonstrates

- Relational database design with keys, constraints, and validation
- SQL aggregation, joins, conditional logic, date calculations, and SLA metrics
- Python data loading, query orchestration, and report generation
- Reproducible analysis with a fixed reporting date
- Automated tests for data integrity and analytics results

## Business questions answered

1. How many tickets are open, resolved, or closed?
2. What percentage met the first-response SLA?
3. Which categories create the most support demand?
4. How do resolution time and satisfaction vary by technician?
5. Which unresolved tickets require attention first?

## Project structure

```text
data/                       Sample technicians and help-desk tickets
sql/schema.sql              SQLite tables, relationships, and constraints
sql/analysis_queries.sql    Named SQL queries used by the report
src/helpdesk_analytics/     Python loader, analytics, CLI, and reporting code
tests/                      Automated tests
sample_report.md            Example output generated from the sample data
```

## Quick start

Requires Python 3.10 or newer. No third-party packages are required.

```bash
PYTHONPATH=src python -m helpdesk_analytics --output helpdesk_report.md
```

The sample report uses `2026-08-31T23:59:59` as the analysis date so backlog
ages stay reproducible. Choose another date with:

```bash
PYTHONPATH=src python -m helpdesk_analytics \
  --as-of 2026-09-06T23:59:59 \
  --output helpdesk_report.md
```

Run the tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Data notes

The dataset is fictional and created only for portfolio demonstration. It
contains no customer, employer, or confidential information. Priorities use
these response targets:

| Priority | First-response target |
|---|---:|
| Critical | 15 minutes |
| High | 30 minutes |
| Medium | 120 minutes |
| Low | 240 minutes |

Satisfaction is recorded from 1 to 5 only for tickets with survey responses.

## Example findings

The included sample report highlights ticket volume, SLA performance, category
trends, technician metrics, and the unresolved backlog. Because the reporting
logic is driven by named SQL queries, each number can be traced directly to its
calculation.

## Possible next steps

- Add monthly trend charts and CSV export
- Compare SLA performance across departments
- Build an interactive dashboard
- Add first-contact resolution and escalation-event tables

