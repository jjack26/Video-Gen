"""Render approved local shot plans without text or branding overlays."""
from pathlib import Path
import subprocess
from .footage import validate_shots

def build_command(plan: dict, output: str) -> list[str]:
    shots = plan['shots']
    validate_shots(shots)
    if plan.get('overlays'):
        raise ValueError('overlays are disabled')
    if not plan.get('concept_approved'):
        raise ValueError('approve the concept before rendering')
    destination = Path(output).resolve()
    command = ['ffmpeg','-hide_banner','-n']
    filters, streams = [], []
    for i, shot in enumerate(shots):
        source = Path(shot['source']).resolve()
        if not source.is_file() or source == destination:
            raise ValueError('source file missing or output conflicts with source')
        if shot.get('keep_audio'):
            raise ValueError('audio editing needs a separately reviewed sound plan; this renderer exports silent previews')
        x = float(shot.get('focus_x', .5))
        if not 0 <= x <= 1:
            raise ValueError('focus_x must be between zero and one')
        command += ['-ss',str(shot['start']),'-t',str(shot['end']-shot['start']),'-i',str(source)]
        filters.append(f'[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)*{x}:0,setsar=1,fps=30,setpts=PTS-STARTPTS[v{i}]')
        streams.append(f'[v{i}]')
    filters.append(''.join(streams)+f'concat=n={len(shots)}:v=1:a=0[out]')
    return command+['-filter_complex',';'.join(filters),'-map','[out]','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(destination)]

def render(plan: dict, output: str) -> None:
    subprocess.run(build_command(plan,output),check=True,timeout=600,capture_output=True)
