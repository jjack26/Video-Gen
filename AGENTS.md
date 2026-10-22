# Codex instructions for Video-Gen

You are implementing a multi-account, human-supervised AI media operations platform.

## Start here
Read docs/ARCHITECTURE.md, docs/AGENT_NETWORK.md, docs/PHASE_2.md, and docs/SETUP.md. Run `python -m unittest discover -s tests -v` before and after changes. Run `python -m src.demo` to inspect the offline prototype.

## Priorities
1. Build transactional PostgreSQL ledger, persistent queue, account-scoped permissions, and authenticated API before unattended operations.
2. Implement real event-driven orchestration with typed contracts, bounded fan-out, provenance, deduplication, and per-account isolated memory.
3. Add cost estimation and reconciliation per provider, idempotent jobs, provider retries, audit logs, and global kill switch.
4. Implement actual OpenAI provider with tests and controlled budgets; do not use a live key during tests.
5. Confirm Higgsfield API access and integrate only documented supported endpoints with credit preflight and human approval.
6. Add an authenticated responsive dashboard for mobile monitoring, group-chat timeline, review queue, and per-account analytics.
7. Connect social publishing only through official supported APIs and account-owner authorization; require review for outbound content.
8. Add storefront builder and monetization experiments after audience validation.

## Nonnegotiable
Never commit or print secrets. Never assume a paid subscription includes API access. No fake identities, unsolicited mass DMs, engagement manipulation, platform verification bypasses, or fabricated analytics. Avoid unnecessary paid calls. Never claim live connections or deployed systems without verification. Keep human approval for public posting, purchases, and outbound messages until policy-compliant workflows are tested.

## Code conventions
Python 3.12+, standard library first. Add tests for every feature. Use clear modules and typed interfaces. Store local runtime state only under gitignored data/. Preserve existing functionality.
