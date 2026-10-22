# Integration readiness

| Integration | Repo status | External action needed |
| --- | --- | --- |
| GitHub | Connected for repository edits; CI workflow committed | Merge reviewed PR after checks |
| Codex | AGENTS.md and setup docs prepared | Install/sign in to Codex and open repository |
| OpenAI | Responses API adapter coded, disabled by default | Configure separate API billing/key securely; enable only with reliable cost control |
| Higgsfield | Video job schema and stub adapter | Verify whether your Higgsfield plan grants API access and obtain documented API details |
| TikTok | No API integration | Authorize owned accounts and obtain approved posting/comment permissions |
| Discord | Not connected | Create server/bot later, with permission-scoped token |
| Metricool | Not connected | Optional; evaluate plan and supported publishing APIs |
| Hosting | Not deployed | Select cloud host, database, job queue, HTTPS, secret manager |
| Website/storefront | Planned | Choose product and business model after audience tests |

GitHub connector access does not give runtime GitHub Actions access to ChatGPT, Higgsfield, TikTok, or OpenAI credentials. Do not store any API key in this repository. Keep manual approval on all outbound activity.
