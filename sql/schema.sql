PRAGMA foreign_keys = ON;

CREATE TABLE technicians (
    technician_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    team TEXT NOT NULL
);

CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY,
    opened_at TEXT NOT NULL,
    resolved_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    priority TEXT NOT NULL CHECK (priority IN ('Critical', 'High', 'Medium', 'Low')),
    category TEXT NOT NULL,
    channel TEXT NOT NULL CHECK (channel IN ('Portal', 'Email', 'Phone', 'Chat')),
    department TEXT NOT NULL,
    technician_id TEXT NOT NULL,
    first_response_minutes INTEGER NOT NULL CHECK (first_response_minutes >= 0),
    satisfaction_score INTEGER CHECK (satisfaction_score BETWEEN 1 AND 5),
    reopened INTEGER NOT NULL DEFAULT 0 CHECK (reopened IN (0, 1)),
    FOREIGN KEY (technician_id) REFERENCES technicians (technician_id),
    CHECK (
        (status IN ('Resolved', 'Closed') AND resolved_at IS NOT NULL)
        OR (status IN ('Open', 'In Progress') AND resolved_at IS NULL)
    )
);

CREATE INDEX idx_tickets_status ON tickets (status);
CREATE INDEX idx_tickets_priority ON tickets (priority);
CREATE INDEX idx_tickets_category ON tickets (category);
CREATE INDEX idx_tickets_technician ON tickets (technician_id);
