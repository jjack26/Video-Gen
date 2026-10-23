"""Creative handoff contract; no claim that a validator invents ideas."""
def review_concept(concept: dict, evidence: dict) -> dict:
    issues = [f'Missing {k}' for k in ('character','setup','escalation','payoff','originality','source_urls') if not concept.get(k)]
    if not evidence.get('cross_platform'):
        issues.append('Research needs three distinct platforms')
    allowed = {s['url'] for s in evidence.get('sources', [])}
    if any(url not in allowed for url in concept.get('source_urls', [])):
        issues.append('Concept cites unverified sources')
    if concept.get('overlays'):
        issues.append('Text and branding overlays are disabled')
    return {'status':'revise' if issues else 'awaiting_human_concept_review','issues':issues,'concept':concept}
