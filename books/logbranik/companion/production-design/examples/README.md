# Reference examples, not a running application

These files are inputs to implementation prompts. They contain illustrative local addresses
and paths. Nginx, Vector and Docker were unavailable in the pack-generation environment;
runtime validation is therefore required by prompts 009–017 and the later full-system gates.
Do not copy them blindly into an existing production virtual host.

`contracts/snapshot-payload.json` is unsigned structural data with a frozen example time,
not a usable production block request. The envelope template deliberately contains no valid
signature. Implementation prompt 018 creates cryptographic golden vectors with test-only keys.

`vector/vector.toml.example` is TOML and must be checked using the selected Vector binary.
Invalid transform inputs are dropped with Vector error metrics in this reference; prompt 010
must make that failure visible and provide bounded quarantine/rotation as appropriate.
The file source checkpoints and disk sink buffer require persistent directories and correct
log-read permissions. A 256 MiB sample buffer is only a lab starting value.

Example timestamps and documentation IP addresses are fixtures. Freeze the clock or replace
timestamps when generating test messages; never increase production TTL limits to accept an
old example. Use the standard library schemas in CONTRACTS.md as authoritative.
