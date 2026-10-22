# Video-Gen architecture

Video-Gen is a modular, human-supervised AI short-video production system.

## Pipeline
Research -> Strategy -> Script -> Storyboard -> Generation -> Quality Control -> Approval -> Publishing -> Analytics.

## Agent boundaries
Each agent has its own system prompt, input/output schema, and scoped persistent memory. The coordinator routes artifacts between agents. Separate prompts do not imply separate models or independent consciousness.

## Safety and operating principles
- No fabricated performance metrics, fake engagement, spam comments, or unauthorized account actions.
- All publishing requires explicit approval until platform access and safeguards are tested.
- Use approved APIs, respect platform terms, copyright, privacy, and disclosure requirements.
- Never commit secrets. API integrations are optional and disabled by default.
- Keep costs bounded using per-run and monthly budgets.
- Keep a traceable record of decisions, outputs, provider charges, and approvals.

## Future integrations
Higgsfield or another licensed video API, OpenAI models, optional n8n workflows, optional Metricool/social publishing, and analytics. Integrations must be independently configurable and should never assume a paid subscription.

## Repository layout
agents/: agent prompts and responsibilities
config/: non-secret configuration
docs/: architecture and operational planning
src/: executable orchestration and memory infrastructure
tests/: automated validation
