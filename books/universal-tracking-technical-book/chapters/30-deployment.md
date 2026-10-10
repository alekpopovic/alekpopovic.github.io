## Chapter 30 - Portable Deployment with Docker Compose and Nginx

The reference deployment runs on any provider that offers Linux hosts, persistent disks, networking, and an off-site backup target. Docker and Docker Compose package the application; Nginx terminates TLS and routes HTTP, WebSocket, static files, uploads, and optional device streams.

![A production topology can use redundant application hosts, PostgreSQL primary/standby, and off-site backups.](../assets/diagrams/deployment.png){width=95%}

### Container images

Build one minimal Go image with all runtime subcommands:

```dockerfile
FROM golang:1 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build \
    -trimpath \
    -ldflags="-s -w" \
    -o /out/tracking-platform \
    ./cmd/tracking-platform

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/tracking-platform /tracking-platform
USER nonroot:nonroot
ENTRYPOINT ["/tracking-platform"]
```

Pin real base-image digests in the implementation. A distroless image improves attack surface but complicates debugging; maintain a separate diagnostic image or host tools rather than adding a shell to production images.

Angular applications are built in CI and served by Nginx or a separate static container.

### Compose topology

A reference production Compose file can define:

```text
postgres
api-a
api-b
worker
scheduler
gps-gateway
nginx
```

PostgreSQL data, uploads, and backup staging use named volumes or explicitly mounted durable paths. The database port is not published publicly. Health checks gate startup, but application code still handles dependency loss after startup.

`depends_on` is not an availability strategy. Processes retry database connection with bounded backoff and expose readiness accurately.

### Configuration and secrets

Use environment variables for non-secret settings and mounted files for secrets:

```text
DATABASE_URL_FILE=/run/secrets/database_url
TOKEN_SIGNING_KEY_FILE=/run/secrets/token_signing_key
BACKUP_ENCRYPTION_KEY_FILE=/run/secrets/backup_key
```

Images are immutable. Configuration changes create a reviewed deployment. Never mount the entire repository or a writable Docker socket into application containers.

### Nginx HTTP routing

A simplified configuration:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream tracking_api {
    server api-a:8080;
    server api-b:8080;
    keepalive 64;
}

server {
    listen 443 ssl http2;
    server_name track.example.com;

    client_max_body_size 10m;

    location /api/ {
        proxy_pass http://tracking_api;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-Id $request_id;
        proxy_read_timeout 60s;
    }

    location /ws {
        proxy_pass http://tracking_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 75s;
    }

    location / {
        root /srv/dashboard;
        try_files $uri $uri/ /index.html;
    }
}
```

Set security headers, TLS policy, request limits, and timeouts appropriate to the actual deployment. Do not trust forwarded headers from arbitrary clients; define trusted proxy boundaries.

### GPS stream routing

Nginx `stream` can proxy TCP and UDP when the installed build supports it:

```nginx
stream {
    upstream teltonika_gateway {
        server gps-gateway:5001;
    }

    server {
        listen 5001;
        proxy_pass teltonika_gateway;
        proxy_timeout 10m;
        proxy_connect_timeout 5s;
    }
}
```

Preserving client address may require the PROXY protocol and gateway support. Validate device behavior through real tests; some trackers have strict connection assumptions.

### Rolling replacement

A provider-neutral rollout can:

1. run migrations in a dedicated command;
2. start new API replicas on alternate ports or hosts;
3. verify readiness and smoke tests;
4. add them to Nginx upstreams;
5. drain old replicas;
6. restart workers and gateway roles;
7. verify queues, realtime, and ingestion;
8. retain the previous image for rollback.

Schema changes must remain compatible throughout the overlap.

### Systemd integration

On hosts, systemd can manage the Compose project or individual containers, ensure startup after storage and networking, and enforce restart policy. Use bounded restart bursts so a configuration failure does not loop indefinitely.

### Filesystem storage

Uploads and generated exports use a storage interface rooted in a mounted path. Safe implementation requires:

- server-generated opaque paths;
- no client path traversal;
- atomic writes and fsync policy;
- checksum verification;
- file type and size validation;
- restricted permissions;
- antivirus or content scanning where required;
- backup and retention integration.

For multiple application hosts, use shared storage or route upload ownership deliberately. The interface allows later object-store adoption without changing domain records.

### Chapter checklist

A portable deployment has:

- immutable minimal images;
- separate application roles;
- private database networking;
- mounted secret files;
- correct HTTP and WebSocket proxy behavior;
- bounded GPS stream routing;
- migration-aware rolling replacement;
- provider-neutral durable file storage;
- a tested rollback procedure.
