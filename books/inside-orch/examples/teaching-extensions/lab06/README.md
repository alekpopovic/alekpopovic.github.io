# Namespace/quota teaching harness

Original book extension; imports the pinned Orch module without changing it. See `labs/06-namespaces-quotas/README.md` for isolated-copy setup and `validation/labs/06-check.json` for 28 actual in-process HTTP/MemoryService observations. It requires the canonical fixture directory as its sole argument. It binds no listener and uses no Docker/database. Concurrent admission applies only to the tested memory implementation. The independent-server test explicitly demonstrates separate active state.
