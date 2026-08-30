# Project ORCA — Infrastructure & Deployment

This directory contains infrastructure-as-code (Terraform), Kubernetes / Helm deployment manifests, and feature flag configurations.

---

## Structure

- `helm/`: Helm chart templates for microservices and API gateways.
- `k8s/`: Base Kubernetes deployment, service, and ingress manifests.
- `feature_flags.yml`: Global and regional feature toggles with safe-mode defaults.
- `terraform/`: Cloud infrastructure modules (PostgreSQL+PostGIS, Timescale, Object Storage, Redis).

---

## Deployment & Safety Policies

- Canary deployments route 5% of traffic initially.
- Automated rollback is triggered on error rate > 2% or threshold violations.
- Direct production modifications are prohibited without Manager and SRE sign-off.
