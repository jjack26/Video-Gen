"""Check shot timing and footage and audio provenance separately."""
from math import isfinite

def validate_shots(shots: list[dict]) -> None:
    if not shots or len(shots)>30:
        raise ValueError('supply 1 to 30 shots')
    for shot in shots:
        start, end = float(shot['start']), float(shot['end'])
        if not isfinite(start) or not isfinite(end) or start<0 or end<=start or end-start>60:
            raise ValueError('invalid shot timing')
        if not shot.get('source') or not shot.get('usage_basis'):
            raise ValueError('footage provenance is required')
        if shot.get('keep_audio') and not shot.get('audio_usage_basis'):
            raise ValueError('audio usage must be checked separately')
