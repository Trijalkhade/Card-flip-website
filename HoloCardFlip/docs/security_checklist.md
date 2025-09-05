# Security Checklist (Must do before public launch)

1. Enforce HTTPS everywhere (HSTS), use strong TLS ciphers.
2. Secrets management: do NOT bake API keys into images. Use Vault or cloud secret stores.
3. Input validation & parameterized DB queries (SQLAlchemy + Pydantic).
4. WAF and rate limiting for public endpoints.
5. Authentication:
   - Refresh token rotation.
   - Revoke tokens on logout.
6. Protect against CSRF for cookie-based flows.
7. Penetration testing + dependency scanning (Snyk/Dependabot).
8. Logging & monitoring: central logs with alerting on suspicious activity.
9. Limit access to DB with least privilege network rules.
10. Backup & recovery plans; encryption at rest & transit.

