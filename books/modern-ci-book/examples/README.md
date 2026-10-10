# Examples and their execution boundaries

| Directory | What exists | Edition 0.1 status |
|---|---|---|
| `lab/` | Standalone Go model and tests | Executed locally; in-memory only |
| `sql/` | PostgreSQL schema and conditional transactions | Illustrative; database execution not performed |
| `pipelines/` | Proposed configuration language | Design examples; no parser is shipped |
| `contracts/` | Example runner result message | Illustrative payload, not a complete schema |

All original code and configuration here is MIT-licensed. Read the book for
contracts, threat boundaries and the missing production components. The
laboratory does not launch containers or network services, store credentials,
or alter cloud resources. An example `runner_id` must never replace an
authenticated peer identity in a real service.
