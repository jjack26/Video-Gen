# Video-Gen Studio

The live GitHub Pages interface is a mobile-friendly workspace for seven separately configured content roles. It is not a deployed agent backend.

## Roles and actual capabilities

Each role has its own file under `agents/`, default brief in `dashboard/team.json`, and implementation in `src/content_agents/`.

- Research validates supplied source observations, dates and platform diversity. Live collection adapters are not deployed.
- Concept validates story structure, evidence references and overlay restrictions. It does not create ideas without a model invocation.
- Footage validates timecodes, footage provenance and separate audio usage basis.
- Editor renders approved local FFmpeg shot plans without overlays. The current renderer outputs silent previews, requires per-shot focus and does not claim to evaluate framing creatively.
- Quality checks the actual encoded output using ffprobe and requires human visual review.
- Publisher prepares a SHA-256-bound packet, defaults to private and rejects public packets without matching approval. This module does not call Metricool.
- Analytics keeps explicit feedback separate from observed metrics.

`src/content_agents/runtime.py` can explicitly invoke the existing OpenAI adapter with an individual brief. Disabled by default. API credentials must be supplied server-side. This invocation has no browser, FFmpeg or publishing tools and reports that limitation to the model. It is not unattended orchestration.

## Commands

`python -m src.content_team brief research`

`python -m src.content_team check-research observations.json`

`python -m src.content_team render approved-plan.json data/preview.mp4`

A render plan contains `concept_approved: true`, `shots`, and no overlays. Each shot needs a local `source`, numeric `start` and `end`, documented `usage_basis`, and `focus_x` from 0 to 1. This renderer supports silent previews only. Keep audio off until a sound plan is reviewed. Run from a trusted local or cloud worker, never execute uploaded arbitrary code.

## Interface

Command room saves directions and copies a structured handoff for ChatGPT or Claude. It does not fabricate GPT replies. Each agent has separate mission, output, constraints, taste, sources, references and feedback fields. Research notes and concept reviews persist on the current device. Workspace export/import transfers these between devices manually. The earlier dashboard remains at `legacy.html` and keeps its existing localStorage keys.

## Phone

Install the manifest-backed web app with Safari Share > Add to Home Screen or Android Install app. Cached briefs are available offline after an online visit. This is a Home Screen app, not a native iOS/Android widget. There is no background execution or cloud sync yet.

## Required before live GPT and desktop-independent work

Deploy an authenticated API, persistent per-user database and queue, object storage, model adapter with hard budget controls, trusted worker with FFmpeg, and official research/publishing connectors. Store secrets in hosting environment configuration. Never put keys or GitHub tokens in the static site. ChatGPT's Metricool OAuth connection and subscription do not transfer to the website. Claude session access has not been connected. A supported server-side Anthropic integration would require a separate authorized API connection and budget.

Agent browser automation in this ChatGPT session is not a worker permanently attached to the site. Configured agents are not simultaneously running models. No new public posts are authorized by editing a brief.

## Independent brains and account isolation

Each role now has an authoritative, individually editable JSON brain in `agents/brains/<role>.json`, a separate Markdown role description and its own code module. Model settings and output contract belong to that role. They can use the same underlying model without sharing prompts or private working memory. These are software agent configurations, not independently trained model weights or consciousness.

`runtime.run_agent` reads only `data/memory/<account_id>/agent/<role>.jsonl` plus explicitly human-reviewed team lessons for that same account. Raw model drafts are marked unverified. New account IDs must have their own configuration under `config/brands/`; unknown accounts are rejected. The first profile is `jmanfire2`. No new social profiles are created by adding configuration.

The browser workspace now saves under an account-scoped key and exports its account identity. Cross-account imports are rejected. UI changes remain local and are not automatically committed into server brain files. The links on each agent show its actual separate brain and code.

`python -m src.content_agents.collect_youtube data/official-cohort.json` collects at most 30 video and 30 Shorts public listing records from the official Clash Royale channel. It requires `yt-dlp` installed in that worker. No video is downloaded and no account authentication is used. Counts can be rounded. This collector is implemented and was run manually in this session, not deployed as an ongoing background job.
