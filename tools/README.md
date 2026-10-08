# tools/

FastMCP tool servers, one per area. Arrives in Phase 4.

Rules every tool follows (see `docs/security.md`):
- it is on the allowlist, or it does not run
- tools that change anything are marked `requires_confirmation` and wait for an explicit yes
- arguments are validated against a schema before running
- every call is written to the append-only audit log
