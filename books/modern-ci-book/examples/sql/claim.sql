-- SPDX-License-Identifier: MIT
-- PREPARE once per session, then EXECUTE with bound values.
-- $1 authorized project, $2 authorized pool, $3 authenticated runner,
-- $4 positive lease duration (maximum five minutes), $5 fresh attempt ID.
-- The caller must enforce dependencies, policy and capacity atomically.
-- Reconnect uncertainty requires a lookup by attempt ID, not a blind new claim.
PREPARE claim_job(text, text, text, interval, text) AS
WITH candidate AS (
    SELECT id FROM jobs
    WHERE project_id = $1 AND pool_id = $2 AND state = 'queued'
      AND ready_at <= statement_timestamp()
      AND $4 > interval '0 seconds' AND $4 <= interval '5 minutes'
    ORDER BY priority DESC, ready_at, id
    FOR UPDATE SKIP LOCKED
    LIMIT 1
), claimed AS (
    UPDATE jobs AS j
    SET state = 'leased', fence = j.fence + 1,
        current_attempt_id = $5, lease_runner = $3,
        lease_until = statement_timestamp() + $4
    FROM candidate AS c
    WHERE j.id = c.id
    RETURNING j.id, j.fence, j.current_attempt_id, j.lease_until
), recorded AS (
    INSERT INTO attempts (id, job_id, fence, runner_id, state)
    SELECT current_attempt_id, id, fence, $3, 'leased' FROM claimed
    RETURNING id
)
SELECT c.* FROM claimed c JOIN recorded a ON a.id = c.current_attempt_id;
