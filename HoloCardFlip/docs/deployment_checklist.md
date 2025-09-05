# Deployment Checklist (before public launch)

1. Move secrets to Vault or cloud secret manager.
2. Provision DB with replica sets, backups.
3. Configure autoscaling on Kubernetes with HPA.
4. Enable HTTPS through cert-manager (Let's Encrypt) and set HSTS.
5. Configure monitoring, alerting & log retention.
6. Run security scans and pentests.
7. Run load tests (k6, locust).
8. Prepare incident response and data-retention policy.
