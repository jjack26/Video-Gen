"""Evidence validation. Collection adapters must supply real observations."""
from datetime import datetime
from urllib.parse import urlsplit

DOMAINS = {'youtube.com':'youtube', 'youtu.be':'youtube', 'tiktok.com':'tiktok', 'instagram.com':'instagram', 'reddit.com':'reddit', 'x.com':'x', 'twitter.com':'x', 'supercell.com':'supercell'}

def review_sources(sources: list[dict]) -> dict:
    verified, rejected, seen = [], [], set()
    for source in sources:
        url = source.get('url', '')
        parsed = urlsplit(url)
        host = (parsed.hostname or '').lower()
        platform = next((v for k,v in DOMAINS.items() if host == k or host.endswith('.'+k)), None)
        try:
            stamp = datetime.fromisoformat(source.get('observed_at', '').replace('Z', '+00:00'))
            valid = stamp.tzinfo is not None and stamp <= datetime.now(stamp.tzinfo)
        except (ValueError, TypeError):
            valid = False
        if parsed.scheme != 'https' or not platform or not valid or not source.get('observation') or url in seen:
            rejected.append(url)
            continue
        seen.add(url)
        verified.append({**source, 'platform':platform})
    platforms = sorted({s['platform'] for s in verified})
    return {'sources':verified, 'rejected':rejected, 'platforms':platforms, 'cross_platform':len(platforms)>=3, 'status':'ready' if len(platforms)>=3 else 'needs_more_evidence'}
