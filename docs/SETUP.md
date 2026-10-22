# Video-Gen setup checklist

## Already prepared
- GitHub repository, agent role definitions, event-routing scaffolds, memory namespaces, budget/approval gates, example accounts, offline demo, unit tests, and GitHub Actions CI.
- OpenAI Responses API adapter code is present but **disabled** unless explicitly invoked. No API key is stored in this repository.
- Higgsfield adapter is an intentional stub. A paid Higgsfield subscription does not automatically imply public API credentials or API access.

## When Codex is available
1. Open the repository in Codex/VS Code and check out the development branch or merge the pull request after CI succeeds.
2. Run `python -m unittest discover -s tests -v`.
3. Run `python -m src.demo --niche technology --account demo_tech` for a zero-cost local agent conversation.
4. For OpenAI live model testing, create an OpenAI API key in the OpenAI developer platform and store it in a local environment variable or approved secret manager. ChatGPT Plus does not fund API calls. Do not paste secrets in chat or commit them.
5. Confirm Higgsfield's account-specific API availability and generation costs. Only then implement an authenticated adapter, estimate credits, and gate every job with approvals and transactionally enforced spending caps.
6. Connect social accounts through official platform OAuth where supported. Account setup, verification, and approvals may require human steps.
7. Deploy a secure database, job queue, dashboard, HTTPS, and transactional spending ledger before unattended operations.

## Cost and safety
- Prototype budget defaults: $2 per run and $30 per month. These limits are **not** enforced across multiple processes and do not guarantee provider billing limits.
- The OpenAI adapter caps output tokens but must be wrapped in a production-grade cost controller and usage reconciliation before unattended use.
- No automatic account creation, commenting, DMing, posting, or purchases are enabled.
- Prefer an organic audience-first strategy. Only offer relevant opt-in products, affiliate offers with disclosures, or a legitimate paid service.

## Current limits
This is a working offline proof-of-concept scaffold, not a deployed autonomous platform. Higgsfield, TikTok, Metricool, Discord, hosting, and paid OpenAI API are not connected to the GitHub code yet.
