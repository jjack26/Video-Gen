# Video-Gen: Multi-Agent Content Operations

## Mission
Build a web-based, mobile-friendly command center that discovers emerging trends from authorized connected social accounts and public data, creates original short-form videos, runs QA, and publishes through approved platform integrations. Never fabricate live metrics or claim a post succeeded without a returned post ID.

## Agents and responsibilities
1. **Trend Scout**: Collect TikTok Creative Center, YouTube, Instagram, Reddit, and public niche signals where officially accessible. Record URL, platform, timestamp, metric definitions, permission scope, and confidence. Never scrape private accounts or bypass restrictions.
2. **Research Analyst**: Compare growth, format, hook, audience fit, competition, and freshness. Separate verified trends from hypotheses. Deduplicate sources.
3. **Strategist**: Rank candidates using source evidence, target audience, production cost, and historical account performance. Recommend experiments rather than promise views.
4. **Scriptwriter**: Produce 9:16 storyboards, opening hooks, visual beats, captions, and relevant hashtags. Avoid copying copyrighted clips.
5. **Production**: Check available free allowances and cost estimates before any paid generation. Generate media with provider adapters (Higgsfield etc.). Record job IDs, provenance, and output URLs.
6. **Quality Control**: Verify format, duration, legibility, audio, originality, and platform policy. Require human approval for initial posts.
7. **Publisher**: Use connected Metricool or official platform API if publishing capability exists. Record destination, scheduled time, post ID, error and retry state. Never assume account connection equals publishing authorization.
8. **Analytics**: Pull account-authorized metrics, normalize time windows, compare experiments, and update evidence-backed recommendations. No fake engagement or artificial boosting.
9. **Orchestrator**: Own task queues, budgets, retries, approvals, audit log, and agent health.

## Pipeline
DISCOVER -> VERIFY -> SCORE -> SCRIPT -> ESTIMATE_COST -> APPROVE_GENERATION -> GENERATE -> QA -> APPROVE_POST -> SCHEDULE -> PUBLISH -> VERIFY_POST -> MEASURE -> LEARN.

## Dashboard requirements
- Dark sci-fi neon blue/green UI with animated, accessible status indicators and reduced-motion setting.
- Live workflow DAG and per-agent status (idle, working, blocked, awaiting approval, failed, done).
- Trend evidence feed with clickable source URLs and observed timestamps.
- Video queue with thumbnail, storyboard, asset/job ID, platform targets, captions, cost estimate, QA, approval and post ID.
- Connected accounts screen with scope and token health, never exposing secrets.
- Editable per-agent instruction/knowledge files and durable memory, with audit trail.
- Analytics by account, platform, video, and experiment; source-backed metrics only.
- Spending limits, daily cap, kill switch, manual approval for initial generation and publishing.

## Technical shape
- Next.js + TypeScript frontend, Python/FastAPI API and worker processes.
- Postgres/Supabase when ready for durable data, task queues, and account-level permissions; development mocks must be clearly labeled DEMO.
- Provider adapters: TikTok Creative Center public trends, authorized TikTok/Metricool, YouTube API, Reddit API, Instagram Graph API where eligible, Higgsfield.
- Deploy backend and workers to cloud for 24/7 operation; GitHub alone does not execute workers.
- Secrets stored in managed secret store/environment only, never in repository or logs.

## Immediate first experiment
Clash Royale-inspired comedic vertical short: 'Hog Rider gets pulled over.' Research source-backed current niche examples before generation. Confirm eligible free video method and official publishing permissions. No paid spend without explicit approval.

## Status (2026-10-22)
Public trend research started. Higgsfield account has 10 credits, pending trial, five free influencer-sheet generations, zero free motion-transfer video generations. Metricool publishing access not yet exposed to this chat. No video generated or post published in this workflow.
