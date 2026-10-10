## Appendix D - Deployment Blueprint

### Compose skeleton

```yaml
services:
  postgres:
    image: postgis/postgis:pin-a-reviewed-version
    restart: unless-stopped
    environment:
      POSTGRES_DB: tracking
      POSTGRES_USER_FILE: /run/secrets/postgres_user
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./postgres/init:/docker-entrypoint-initdb.d:ro
    secrets:
      - postgres_user
      - postgres_password
    networks: [data]

  api-a:
    image: registry.example/tracking-platform:${TRACKING_VERSION}
    command: ["api"]
    env_file: [./config/common.env, ./config/api.env]
    secrets: [database_url, token_signing_key]
    depends_on: [postgres]
    networks: [edge, data]

  api-b:
    extends: api-a

  worker:
    image: registry.example/tracking-platform:${TRACKING_VERSION}
    command: ["worker"]
    env_file: [./config/common.env, ./config/worker.env]
    secrets: [database_url]
    depends_on: [postgres]
    networks: [data]

  scheduler:
    image: registry.example/tracking-platform:${TRACKING_VERSION}
    command: ["scheduler"]
    env_file: [./config/common.env]
    secrets: [database_url]
    depends_on: [postgres]
    networks: [data]

  gps-gateway:
    image: registry.example/tracking-platform:${TRACKING_VERSION}
    command: ["gps-gateway"]
    env_file: [./config/common.env, ./config/gateway.env]
    secrets: [database_url]
    depends_on: [postgres]
    networks: [edge, data]

  nginx:
    image: nginx:pin-a-reviewed-version
    ports:
      - "443:443"
      - "5001:5001"
    volumes:
      - ./nginx:/etc/nginx:ro
      - ./tls:/etc/nginx/tls:ro
      - dashboard-static:/srv/dashboard:ro
    depends_on: [api-a, api-b, gps-gateway]
    networks: [edge]

networks:
  edge:
  data:
    internal: true

volumes:
  postgres-data:
  dashboard-static:

secrets:
  postgres_user:
    file: ./secrets/postgres_user
  postgres_password:
    file: ./secrets/postgres_password
  database_url:
    file: ./secrets/database_url
  token_signing_key:
    file: ./secrets/token_signing_key
```

The exact image tags must be pinned to reviewed versions or digests. Do not publish the database port. `extends` support and production tooling should be verified in the selected Compose implementation.

### Deployment sequence

```text
preflight configuration and disk space
verify backup and WAL archive health
pull immutable image by digest
run migration plan and compatible migrations
start new API instances
run readiness and smoke tests
switch or expand Nginx upstreams
drain old API instances
replace workers and scheduler
replace GPS gateway carefully
verify ingest, realtime, jobs, and alerts
record release evidence
```

### Rollback

Application rollback is safe only while the schema remains backward compatible. A release plan states:

- previous image digest;
- minimum compatible migration version;
- whether new writes can be read by old code;
- whether workers must be paused;
- how to drain active WebSockets;
- how to verify restored service;
- when database PITR is the only option.
