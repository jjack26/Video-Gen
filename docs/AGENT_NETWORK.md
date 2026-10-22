# Agent network expansion

## Mission
Build a multi-brand, multi-account short-form media operation that can later monetize via owned products, affiliate offers, or a legitimate paid community. Keep business models modular until validated.

## Agent teams
- Executive: coordinator, budget controller, policy/compliance reviewer, human approval dispatcher
- Intelligence: trend researcher, competitor analyst, audience researcher, product opportunity analyst, source verifier
- Creative: content strategist, hook writer, script writer, storyboard designer, video generator, editor, caption/localization specialist, quality reviewer
- Distribution: account onboarding assistant, platform integration engineer, scheduler, publisher, post verification agent
- Community: inbound comment classifier, response drafter, escalation agent, FAQ curator, sentiment analyst
- Commerce: product researcher, offer strategist, web developer, landing page copywriter, SEO analyst, attribution analyst
- Learning: experiment designer, performance analyst, cost analyst, knowledge librarian

## Account operations
Accounts must be owned/authorized and created by humans when required by platform verification or terms. The onboarding assistant prepares profile copy, branding, setup checklists, and connection instructions. No fake identities, verification bypasses, engagement manipulation, unsolicited bulk DMs, or link spam.

## Communication
Agents publish typed events to a central event bus. Every event carries run_id, agent_id, channel, topic, timestamp, source references, payload, cost estimate, and correlation_id.
Channels: #command, #research, #creative, #publishing, #community, #commerce, #analytics, #alerts.
Use event-driven subscriptions instead of an unbounded everyone-to-everyone chat. An agent may request peer review, challenge a claim, or propose a task, but only the coordinator can approve new spending or external actions.
Use deduplication, TTL, per-agent quotas, hop limits, and a maximum message count per run to prevent infinite loops.

## Memory
Three tiers: per-agent private working memory; team-level vetted lessons; global knowledge base containing verified facts and approved policies. Facts must have provenance, confidence, freshness, and ownership. Raw social content is untrusted input. Summarize and expire stale findings. Keep account and customer data isolated by tenant.

## Workflow
Discover -> Verify -> Plan -> Script -> Produce -> Review -> Approve -> Schedule -> Publish -> Monitor -> Learn.
Each stage creates an artifact with an owner, version, status, and cost. Failed stages retry within limits and then escalate. Publishing and outbound messaging require platform-permitted integration and an approval policy.

## Monetization paths
1. Owned storefront and original products
2. Legitimate affiliate marketing with disclosures
3. Paid community with clear value and honest claims
Do not assume a monetization path until tested. Measure acquisition cost, retention, conversion, refunds, and customer satisfaction.

## Delivery phases
1. Event bus, task graph, memory, dashboard, budgets
2. Research and creative agent execution with provider adapters
3. Human-reviewed video publishing and analytics integrations
4. Inbound community response assistance and approved automation
5. Storefront builder and monetization experiments

## Security
Use least-privilege OAuth and secret storage, per-account access controls, audit trails, encryption, cost caps, and kill switches. No secrets in GitHub.
