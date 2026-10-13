# ch40-source-anchor

Verify build/test/lint/release contracts and distinguish skipped checks. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [.github/workflows/ci.yml, lines 11–30](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/.github/workflows/ci.yml#L11-L30).

```yaml
jobs:
  quality:
    name: Format, Lint, Vet, Test
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: orch
          POSTGRES_USER: orch
          POSTGRES_PASSWORD: orch
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U orch -d orch"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 10
    env:
      ORCH_E2E_DATABASE_URL: postgres://orch:orch@localhost:5432/orch?sslmode=disable
```

SHA-256: `cffc82040c130216cdcecc708472a3e52d1e362b5e092ab6a0597932b8f53868`. This excerpt is not an independently compilable program.
