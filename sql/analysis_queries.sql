-- name: executive_summary
SELECT
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS completed_tickets,
    SUM(CASE WHEN status IN ('Open', 'In Progress') THEN 1 ELSE 0 END) AS open_backlog,
    ROUND(AVG(CASE
        WHEN resolved_at IS NOT NULL
        THEN (julianday(resolved_at) - julianday(opened_at)) * 24
    END), 1) AS avg_resolution_hours,
    ROUND(100.0 * AVG(CASE
        WHEN first_response_minutes <= CASE priority
            WHEN 'Critical' THEN 15
            WHEN 'High' THEN 30
            WHEN 'Medium' THEN 120
            WHEN 'Low' THEN 240
        END THEN 1.0 ELSE 0.0
    END), 1) AS first_response_sla_pct,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM tickets;

-- name: category_performance
SELECT
    category,
    COUNT(*) AS ticket_count,
    SUM(CASE WHEN status IN ('Open', 'In Progress') THEN 1 ELSE 0 END) AS open_count,
    ROUND(AVG(CASE
        WHEN resolved_at IS NOT NULL
        THEN (julianday(resolved_at) - julianday(opened_at)) * 24
    END), 1) AS avg_resolution_hours,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
FROM tickets
GROUP BY category
ORDER BY ticket_count DESC, category;

-- name: priority_sla
SELECT
    priority,
    COUNT(*) AS ticket_count,
    SUM(CASE
        WHEN first_response_minutes <= CASE priority
            WHEN 'Critical' THEN 15
            WHEN 'High' THEN 30
            WHEN 'Medium' THEN 120
            WHEN 'Low' THEN 240
        END THEN 1 ELSE 0
    END) AS within_sla,
    ROUND(100.0 * AVG(CASE
        WHEN first_response_minutes <= CASE priority
            WHEN 'Critical' THEN 15
            WHEN 'High' THEN 30
            WHEN 'Medium' THEN 120
            WHEN 'Low' THEN 240
        END THEN 1.0 ELSE 0.0
    END), 1) AS sla_pct
FROM tickets
GROUP BY priority
ORDER BY CASE priority
    WHEN 'Critical' THEN 1
    WHEN 'High' THEN 2
    WHEN 'Medium' THEN 3
    WHEN 'Low' THEN 4
END;

-- name: technician_performance
SELECT
    tech.name AS technician,
    tech.team,
    COUNT(t.ticket_id) AS assigned_tickets,
    SUM(CASE WHEN t.status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS completed_tickets,
    ROUND(AVG(CASE
        WHEN t.resolved_at IS NOT NULL
        THEN (julianday(t.resolved_at) - julianday(t.opened_at)) * 24
    END), 1) AS avg_resolution_hours,
    ROUND(AVG(t.satisfaction_score), 2) AS avg_satisfaction,
    SUM(t.reopened) AS reopened_tickets
FROM technicians AS tech
LEFT JOIN tickets AS t ON t.technician_id = tech.technician_id
GROUP BY tech.technician_id, tech.name, tech.team
ORDER BY completed_tickets DESC, technician;

-- name: channel_volume
SELECT
    channel,
    COUNT(*) AS ticket_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM tickets), 1) AS share_pct
FROM tickets
GROUP BY channel
ORDER BY ticket_count DESC, channel;

-- name: open_backlog
SELECT
    ticket_id,
    priority,
    category,
    status,
    department,
    tech.name AS technician,
    CAST(julianday(:as_of) - julianday(opened_at) AS INTEGER) AS age_days
FROM tickets AS t
JOIN technicians AS tech ON tech.technician_id = t.technician_id
WHERE status IN ('Open', 'In Progress')
ORDER BY CASE priority
    WHEN 'Critical' THEN 1
    WHEN 'High' THEN 2
    WHEN 'Medium' THEN 3
    WHEN 'Low' THEN 4
END, opened_at;

