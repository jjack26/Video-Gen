"""Load one independent brain and optionally its account-specific configuration."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[2]
SAFE_ID=re.compile(r'^[A-Za-z0-9_-]{1,64}$')
AGENT_IDS=frozenset({'research','concept','footage','editor','quality','publisher','analytics'})

def load_brief(agent_id: str, account_id: str | None=None) -> dict:
    if agent_id not in AGENT_IDS:
        raise ValueError('unknown content agent')
    brief=json.loads((ROOT/'agents/brains'/f'{agent_id}.json').read_text())
    if account_id is not None:
        if not SAFE_ID.fullmatch(account_id):
            raise ValueError('invalid account id')
        profile=ROOT/'config/brands'/f'{account_id}.json'
        if not profile.is_file():
            raise ValueError('account has no independent profile')
        account=json.loads(profile.read_text())
        brief.update(account.get('agent_overrides',{}).get(agent_id,{}))
        brief['account_id']=account_id
        brief['account_direction']=account['creative_direction']
        brief['account_niche']=account['niche']
    return brief
