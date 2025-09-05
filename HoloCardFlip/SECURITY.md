# Security Guide (summary)

- Use parameterized queries (no f-strings for SQL).
- Store secrets in secret manager; inject at runtime.
- Rotating JWT signing keys periodically.
- Use TLS for all services; do not expose DB ports publicly.
- Implement CSP and security headers via reverse proxy.
