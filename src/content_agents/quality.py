"""Technical checks never substitute for independent visual review."""
import json
import subprocess

def inspect_video(path: str, plan: dict) -> dict:
    result = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path],capture_output=True,text=True,check=True,timeout=30)
    metadata = json.loads(result.stdout)
    video = next(s for s in metadata['streams'] if s['codec_type']=='video')
    issues=[]
    if video['width']*16 != video['height']*9:
        issues.append('Video must be 9:16')
    if not 1 <= float(metadata['format']['duration']) <= 60:
        issues.append('Duration outside 1 to 60 seconds')
    if plan.get('overlays'):
        issues.append('Overlays violate creative preferences')
    return {'status':'revise' if issues else 'awaiting_visual_review','issues':issues,'metadata':metadata,'human_preview_approved':False}
