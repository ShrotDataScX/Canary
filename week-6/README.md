# Week 6: Deploy & Present

> **Status: outline.** Detailed resources will be added after Week 5.

## Goal
Ship Canary and its harness as a **deployed service**, with the harness acting as the release gate, then present the results.

## Planned topics
- **API** (FastAPI) and a simple **UI** (e.g. Streamlit/Gradio)
- **Containerization** (Docker), configuration and secrets management
- **CI/CD**: run unit tests + the harness on every PR; block deploys on regression
- Hosting options and cost trade-offs; deployment to a cloud/PaaS target
- **Monitoring & observability**: request logging (without leaking secrets/PII), latency, cost, guardrail triggers, data-freshness jobs
- Scheduled **data refresh** (daily KEV/NVD, new filings)
- Final **demo, report and retrospective**

## Expected deliverables
- Live deployed endpoint + UI (access controlled as the team decides)
- `deploy/` with Dockerfile, CI workflows and a runbook
- Final report: architecture, harness results (accuracy + attack success rates), lessons learned, future work
- 15-minute team demo

## Prerequisite
Passing harness results from [Week 5](../week-5/README.md).
