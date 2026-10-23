import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.content_agents import load_brief
from src.content_agents.research import review_sources
from src.content_agents.concept import review_concept
from src.content_agents.footage import validate_shots
from src.content_agents.editor import build_command,render
from src.content_agents.publisher import prepare_packet
from src.content_agents.runtime import run_agent
from src.llm_provider import ProviderDisabled

class ContentTeamTests(unittest.TestCase):
    def test_distinct_briefs_and_disabled_api(self):
        self.assertNotEqual(load_brief('research')['mission'],load_brief('editor')['mission'])
        with self.assertRaises(ProviderDisabled):run_agent('concept','Invent a story')
    def test_platform_evidence_not_counted_from_repeated_urls(self):
        source={'url':'https://youtube.com/watch?v=x','observed_at':'2026-01-01T12:00:00Z','observation':'Visible animation'}
        result=review_sources([source,source,{**source,'url':'https://youtube.com.evil.test/'}])
        self.assertEqual(len(result['sources']),1)
        self.assertFalse(result['cross_platform'])
    def test_missing_research_blocks_concept(self):
        self.assertEqual(review_concept({},review_sources([]))['status'],'revise')
    def test_audio_and_nan_require_validation(self):
        with self.assertRaises(ValueError):validate_shots([{'start':0,'end':2,'source':'file','usage_basis':'uploaded','keep_audio':True}])
        with self.assertRaises(ValueError):validate_shots([{'start':0,'end':float('nan'),'source':'file','usage_basis':'uploaded'}])
    def test_editor_rejects_overlay_and_unapproved_work(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'source.mp4';source.touch()
            plan={'shots':[{'source':str(source),'start':0,'end':1,'usage_basis':'test'}]}
            with self.assertRaises(ValueError):build_command(plan,str(Path(folder)/'out.mp4'))
            plan.update(concept_approved=True,overlays=['username'])
            with self.assertRaises(ValueError):build_command(plan,str(Path(folder)/'out.mp4'))
    def test_public_approval_is_bound_to_file_caption_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'preview.mp4';path.write_bytes(b'preview')
            packet=prepare_packet(str(path),'caption','account')
            self.assertEqual(packet['privacy'],'SELF_ONLY')
            approval={k:packet[k] for k in ('sha256','caption','destination','privacy')};approval['privacy']='PUBLIC_TO_EVERYONE'
            self.assertEqual(prepare_packet(str(path),'caption','account',privacy='PUBLIC_TO_EVERYONE',approval=approval)['status'],'prepared_not_posted')
            with self.assertRaises(ValueError):prepare_packet(str(path),'changed','account',privacy='PUBLIC_TO_EVERYONE',approval=approval)
    def test_render_command_uses_no_shell_or_text_filters(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'source.mp4';path.touch()
            plan={'concept_approved':True,'shots':[{'source':str(path),'start':0,'end':1,'usage_basis':'test'}]}
            command=build_command(plan,str(Path(folder)/'out.mp4'))
            self.assertIn('-an',command)
            self.assertNotIn('drawtext',' '.join(command))
            with patch('src.content_agents.editor.subprocess.run') as run:
                render(plan,str(Path(folder)/'out.mp4'))
                self.assertNotIn('shell',run.call_args.kwargs)

class BrainIsolationTests(unittest.TestCase):
    def test_briefs_are_separate_files(self):
        from src.content_agents import ROOT,AGENT_IDS
        import json
        for agent_id in AGENT_IDS:
            brain=json.loads((ROOT/'agents/brains'/f'{agent_id}.json').read_text())
            self.assertEqual(brain['id'],agent_id)
            self.assertTrue((ROOT/'src/content_agents'/f'{agent_id}.py').is_file())
        with self.assertRaises(ValueError):load_brief('editor','../other')
        with self.assertRaises(ValueError):load_brief('editor','unconfigured_account')
    def test_one_agent_does_not_receive_anothers_memory(self):
        from src.memory_store import MemoryStore
        from src.content_agents.runtime import run_agent,share_lesson
        with tempfile.TemporaryDirectory() as folder:
            memory=MemoryStore(folder)
            memory.append('jmanfire2','agent','editor','EDITOR PRIVATE NOTE','test',1)
            memory.append('another_account','agent','research','OTHER ACCOUNT NOTE','test',1)
            with self.assertRaises(ValueError):share_lesson('jmanfire2','unreviewed','test',memory=memory)
            share_lesson('jmanfire2','REVIEWED LESSON','human feedback',approved=True,memory=memory)
            with patch('src.content_agents.runtime.draft_text',return_value='Research draft') as call:
                result=run_agent('research','Find evidence',enabled=True,memory=memory)
                prompt=call.call_args.args[1]
                self.assertNotIn('EDITOR PRIVATE NOTE',prompt)
                self.assertNotIn('OTHER ACCOUNT NOTE',prompt)
                self.assertIn('REVIEWED LESSON',prompt)
            self.assertEqual(result['account_id'],'jmanfire2')
            self.assertEqual(len(memory.read('jmanfire2','agent','research')),1)
            self.assertEqual(len(memory.read('jmanfire2','agent','editor')),1)

class CollectorTests(unittest.TestCase):
    def test_verified_channel_missing_metrics_and_no_fabricated_zero(self):
        from src.content_agents.collect_youtube import normalize_channel,CHANNEL
        data={'channel_id':CHANNEL,'entries':[{'id':'abcdefghijk','title':'clip'}]}
        item=normalize_channel(data,'shorts','2026-10-23T00:00:00Z')[0]
        self.assertIsNone(item['view_count_snapshot'])
        self.assertIsNone(item['published_at'])
        self.assertEqual(item['analysis_status'],'metadata_only_not_watched')
        self.assertTrue(item['counts_may_be_rounded'])
        with self.assertRaises(ValueError):normalize_channel({**data,'channel_id':'fake'},'shorts','now')
    def test_collector_drops_unexpected_ids(self):
        from src.content_agents.collect_youtube import normalize_channel,CHANNEL
        self.assertEqual(normalize_channel({'channel_id':CHANNEL,'entries':[{'id':'../../bad'}]},'videos','now'),[])
