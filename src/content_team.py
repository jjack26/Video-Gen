"""Inspect independently configured agents or render an approved local edit plan."""
import argparse
import json
from pathlib import Path
from .content_agents import load_brief
from .content_agents.editor import render
from .content_agents.research import review_sources

def main():
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest='action',required=True)
    brief=sub.add_parser('brief'); brief.add_argument('agent')
    research=sub.add_parser('check-research'); research.add_argument('file')
    edit=sub.add_parser('render'); edit.add_argument('plan'); edit.add_argument('output')
    args=parser.parse_args()
    if args.action=='brief':
        print(json.dumps(load_brief(args.agent),indent=2))
    elif args.action=='check-research':
        print(json.dumps(review_sources(json.loads(Path(args.file).read_text())),indent=2))
    else:
        render(json.loads(Path(args.plan).read_text()),args.output)

if __name__=='__main__':
    main()
