"""Independent content-stage validators and an actual local FFmpeg editor."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

def load_brief(agent_id: str) -> dict:
    agents = json.loads((ROOT / 'dashboard/team.json').read_text())['agents']
    for brief in agents:
        if brief['id'] == agent_id:
            return dict(brief)
    raise ValueError('unknown content agent')
