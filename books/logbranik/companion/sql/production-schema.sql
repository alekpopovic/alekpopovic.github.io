-- Teaching schema, not an executed PostgreSQL migration or a complete application.
CREATE TABLE guard_events (
    node_id text NOT NULL,
    request_id text NOT NULL CHECK (request_id ~ '^[0-9a-f]{32}$'),
    ingress_hash bytea NOT NULL CHECK (octet_length(ingress_hash) = 32),
    site_id text NOT NULL,
    client_ip inet NOT NULL,
    event_time timestamptz NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    event jsonb NOT NULL,
    PRIMARY KEY (node_id, request_id)
);
CREATE INDEX guard_events_lookup ON guard_events (site_id, client_ip, event_time);

CREATE TABLE detector_jobs (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    node_id text NOT NULL,
    request_id text NOT NULL,
    completed_at timestamptz,
    UNIQUE (node_id, request_id),
    FOREIGN KEY (node_id, request_id) REFERENCES guard_events (node_id, request_id)
);
CREATE INDEX detector_jobs_pending ON detector_jobs (id) WHERE completed_at IS NULL;

CREATE TABLE guard_decisions (
    decision_id uuid PRIMARY KEY,
    site_id text NOT NULL,
    client_ip inet NOT NULL,
    issued_at timestamptz NOT NULL,
    expires_at timestamptz NOT NULL,
    revoked_at timestamptz,
    reason_code text NOT NULL,
    evidence jsonb NOT NULL,
    CHECK (expires_at > issued_at)
);

CREATE TABLE agent_streams (
    agent_id text PRIMARY KEY,
    epoch uuid NOT NULL,
    revision bigint NOT NULL CHECK (revision >= 0)
);
CREATE TABLE policy_deliveries (
    agent_id text NOT NULL REFERENCES agent_streams(agent_id),
    revision bigint NOT NULL CHECK (revision > 0),
    envelope bytea NOT NULL,
    payload_sha256 bytea NOT NULL CHECK (octet_length(payload_sha256) = 32),
    created_at timestamptz NOT NULL DEFAULT now(),
    next_attempt_at timestamptz NOT NULL DEFAULT now(),
    applied_at timestamptz,
    attempts integer NOT NULL DEFAULT 0,
    PRIMARY KEY (agent_id, revision)
);
-- Registration, scopes, detector state, idempotency, audit, quarantine and
-- retention are separate required production migrations in the source pack.
