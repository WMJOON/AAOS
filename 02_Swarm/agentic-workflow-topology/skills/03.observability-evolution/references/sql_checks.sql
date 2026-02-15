-- Recent status distribution
SELECT status, COUNT(*) AS cnt
FROM audit_logs
GROUP BY status
ORDER BY cnt DESC;

-- Retry-like signals (transition_repeated)
SELECT id, date, task_name, mode, status, transition_repeated, notes
FROM audit_logs
WHERE transition_repeated = 1
ORDER BY date DESC
LIMIT 30;

-- Open followups
SELECT id, date, task_name, mode, continuation_hint
FROM v_open_followups
LIMIT 30;

-- Frequently referenced files by agent
SELECT file_path, reference_count, last_referenced
FROM v_agent_document_frequency
LIMIT 30;
