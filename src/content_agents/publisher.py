"""Prepare exact-file publishing packets. No network or automatic publication."""
import hashlib
from pathlib import Path

def prepare_packet(path: str, caption: str, destination: str, *, privacy: str='SELF_ONLY', approval: dict | None=None) -> dict:
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if privacy not in {'SELF_ONLY','PUBLIC_TO_EVERYONE'}:
        raise ValueError('unsupported privacy')
    if not destination:
        raise ValueError('destination required')
    if privacy == 'PUBLIC_TO_EVERYONE' and approval != {'sha256':digest,'caption':caption,'destination':destination,'privacy':privacy}:
        raise ValueError('public posting requires approval of this exact packet')
    return {'sha256':digest,'caption':caption,'destination':destination,'privacy':privacy,'status':'prepared_not_posted'}
