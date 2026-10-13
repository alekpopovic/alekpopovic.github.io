# GitOps/jobs/cron teaching harness

Original book extension; imports the pinned module without changing it. See `labs/07-gitops-jobs-cron/README.md` and `validation/labs/07-check.json` for 26 actual cases. Pass the canonical fixture directory. Real local Git and actual CLI parsers are used; task reports, latest-log transport and cron clock/store are injected. No container execution, network client or durable occurrence deduplication is claimed. Generated repositories/checkouts are uniquely owned and removed.
