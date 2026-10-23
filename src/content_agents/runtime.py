"""Explicit model invocation with role-specific instructions and scoped memory."""
import json
from . import load_brief
from ..llm_provider import draft_text


def run_agent(agent_id: str, task: str, *, enabled: bool=False, context: dict | None=None) -> dict:
    brief=load_brief(agent_id)
    instructions='\n\n'.join([brief['mission'],'Required output: '+brief['output'],'Taste: '+brief['taste'],'Limits: '+brief['constraints'],'Lessons: '+brief['memory']])
    prompt=json.dumps({'task':task,'provided_context':context or {},'available_tools':[], 'instruction':'Work only from supplied evidence. You have no browsing, rendering or publishing tools in this model invocation. Report missing tools and inputs instead of pretending to use them.'})
    answer=draft_text(instructions,prompt,enabled=enabled,max_output_tokens=600)
    return {'agent_id':agent_id,'answer':answer,'status':'draft_requires_review','external_actions_performed':False}
