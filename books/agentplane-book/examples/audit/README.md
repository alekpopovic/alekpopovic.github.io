# Audit Chain Teaching Example

```sh
python3 examples/audit/audit_chain.py
python3 -m unittest discover -s examples/audit -v
```

The verifier requires a caller-supplied **trusted checkpoint**, containing both
count and chain head. Tests demonstrate mutation, truncation, insertion,
reordering and rewriting under a different checkpoint. No private signing key,
public verification service, storage retention or multi-writer protocol is
implemented here. A checkpoint supplied by the same attacker as the log is not
independent evidence. Use only synthetic metadata in this exercise.
