# Phase 2: Hybrid multi-account core

Implemented: in-process bounded agent routing; distinct account definitions; account/agent scoped local memory; per-run and monthly budget reservations; explicit one-time external-action approvals; tests.

Not implemented: persistent database, authentication, actual provider integrations, real account provisioning, TikTok API publishing, production queue, dashboard, cloud deployment, secure multi-user tenancy, durable billing reconciliation, or live agent execution. No social accounts have been created and no API credits have been spent.

Important limitations: local JSONL memory and in-memory budgets are development scaffolds only. They are not safe for concurrent production workers. Budget state must be stored transactionally with atomic reservations and provider charge reconciliation before enabling paid generation. Event payloads must be validated, authenticated, and isolated by account before deployment. Approval IDs must be bound to immutable action payload hashes and authenticated human identities before external actions are enabled.

Hybrid strategy: build audience-first accounts in distinct niches, measure organic performance, then test a transparent store, affiliate offer, or paid community when evidence supports it. Avoid unsolicited outreach, fake identities, or artificial engagement.

Run tests locally: python -m unittest discover -s tests -v
