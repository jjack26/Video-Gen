"""Bounded public-metadata collection from the verified official Clash Royale channel."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

CHANNEL='UC_F8DoJf9MZogEOU51TpTbQ'
VIDEO_ID=re.compile(r'^[A-Za-z0-9_-]{11}$')

def normalize_channel(data: dict, surface: str, observed_at: str) -> list[dict]:
    if data.get('channel_id') != CHANNEL or surface not in {'videos','shorts'}:
        raise ValueError('expected verified official channel and known surface')
    records=[]
    for position,entry in enumerate(data.get('entries',[])[:30],start=1):
        video_id=entry.get('id','')
        if not VIDEO_ID.fullmatch(video_id):
            continue
        count=entry.get('view_count')
        if count is not None and (isinstance(count,bool) or not isinstance(count,(int,float)) or count<0):
            count=None
        records.append({'video_id':video_id,'channel_id':CHANNEL,'creator':'Clash Royale','surface':surface,'listing_position':position,'title':entry.get('title',''),'url':'https://www.youtube.com/'+('shorts/' if surface=='shorts' else 'watch?v=')+video_id,'duration_seconds':entry.get('duration'),'published_at':None,'observed_at':observed_at,'view_count_snapshot':count,'counts_may_be_rounded':True,'likes':None,'retention':None,'paid_organic_split':None,'analysis_status':'metadata_only_not_watched','usage_status':'reference_only_not_cleared_for_reupload'})
    return records

def collect(surface: str) -> list[dict]:
    if surface not in {'videos','shorts'}:
        raise ValueError('unknown surface')
    command=[sys.executable,'-m','yt_dlp','--flat-playlist','--playlist-end','30','--socket-timeout','20','--retries','0','--dump-single-json',f'https://www.youtube.com/channel/{CHANNEL}/{surface}']
    result=subprocess.run(command,capture_output=True,text=True,check=True,timeout=120)
    return normalize_channel(json.loads(result.stdout),surface,datetime.now(timezone.utc).isoformat())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('output');args=parser.parse_args()
    records=collect('videos')+collect('shorts')
    Path(args.output).write_text(json.dumps({'records':records,'limitations':'Public listing snapshots, potentially rounded counts. Missing dates, retention and promotion split. No visual review or performance causality established.'},indent=2)+'\n')

if __name__=='__main__':main()
