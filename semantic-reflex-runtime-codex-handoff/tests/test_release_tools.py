"""Structure-only unit tests. Fixtures deliberately are NOT real Codex evidence."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_e0_evidence as e0
import probe_host
import verify_package


class EvidenceStructureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.trace = self.root / 'test-only-fabricated-shape.txt'
        self.trace.write_text('SYNTHETIC UNIT TEST DATA. NOT A CODEX TRACE.\n', encoding='utf-8')
        digest = e0.file_sha(self.trace)
        self.doc = {
            'schema': 'srr.codex-e0-evidence/1', 'release_id': 'unit-test-only',
            'host': {'name': 'Codex CLI', 'version': 'fixture-0.0.0',
                     'entrypoint_sha256': 'a'*64, 'native_config_sha256': 'b'*64,
                     'run_manifest_sha256': 'c'*64, 'distribution_ref': 'unit-test-only-not-real',
                     'provider_build': 'unit-test-build', 'mcp_sdk_version': 'fixture-0.0'},
            # REAL_CODEX_CAPTURE is deliberately only a field value here. The tool
            # must NEVER claim a real integration PASS even for structurally complete files.
            'cases': [{'case_id': cid, 'status': 'PASS', 'evidence_kind': 'REAL_CODEX_CAPTURE',
                       'expected': 'structural example', 'observed': 'structural example',
                       'limitations': 'all fixture records are synthetic', 'reviewer': 'unit-test-not-human',
                       'artifacts': [{'path': self.trace.name, 'sha256': digest}]} for cid in e0.CASE_IDS]
        }

    def test_complete_structure_does_not_verify_host(self):
        result = e0.report(self.doc, self.root)
        self.assertEqual(result['documentation_status'], 'READY_FOR_HUMAN_REVIEW')
        self.assertIs(result['e0_verified'], False)
        self.assertIs(result['automatic_activation'], False)

    def test_missing_version_rejected(self):
        self.doc['host']['version'] = None
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_latest_not_a_version_lock(self):
        self.doc['host']['version'] = 'latest'
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_missing_distribution_rejected(self):
        self.doc['host']['distribution_ref'] = ''
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_bad_hash_rejected(self):
        self.doc['host']['entrypoint_sha256'] = 'approximate'
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_missing_case_rejected(self):
        self.doc['cases'].pop(0)
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_duplicate_case_rejected(self):
        self.doc['cases'].append(copy.deepcopy(self.doc['cases'][0]))
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_isolation_not_omitted(self):
        self.doc['cases'].pop()
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_h12_cannot_be_na(self):
        next(x for x in self.doc['cases'] if x['case_id'] == 'H12')['status'] = 'N/A'
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_synthetic_kind_not_pass(self):
        self.doc['cases'][0]['evidence_kind'] = 'SYNTHETIC'
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_no_artifact_rejected(self):
        self.doc['cases'][0]['artifacts'] = []
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_tampered_artifact_rejected(self):
        self.trace.write_text('changed', encoding='utf-8')
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_missing_review_rejected(self):
        self.doc['cases'][0]['reviewer'] = None
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_path_traversal_rejected(self):
        self.doc['cases'][0]['artifacts'][0]['path'] = '../outside.txt'
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_absolute_path_rejected(self):
        self.doc['cases'][0]['artifacts'][0]['path'] = str(self.trace)
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_symlink_rejected(self):
        alias = self.root / 'alias.txt'
        alias.symlink_to(self.trace)
        self.doc['cases'][0]['artifacts'][0]['path'] = alias.name
        self.assertTrue(e0.validate(self.doc, self.root))

    def test_invalid_container_rejected(self):
        self.assertTrue(e0.validate([], self.root))

    def test_unfilled_package_template_rejected(self):
        package = Path(__file__).resolve().parents[1]
        doc = json.loads((package / 'config/e0-evidence.template.json').read_text())
        result = e0.report(doc, package)
        self.assertEqual(result['documentation_status'], 'NOT_READY')
        self.assertFalse(result['e0_verified'])


class ProbeTests(unittest.TestCase):
    @patch('probe_host.shutil.which', return_value=None)
    @patch('probe_host.subprocess.run')
    def test_absence_is_observation_not_pass(self, run, which):
        result = probe_host.probe()
        self.assertFalse(result['codex_found'])
        self.assertFalse(result['integration_verified'])
        self.assertEqual(result['status'], 'CODEX_NOT_FOUND')
        run.assert_not_called()

    def test_default_never_executes_found_binary(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / 'fixture-entrypoint'
            f.write_text('this is not an executable host')
            with patch('probe_host.shutil.which', return_value=str(f)), patch('probe_host.subprocess.run') as run:
                result = probe_host.probe()
                self.assertTrue(result['codex_found'])
                self.assertEqual(result['entrypoint_sha256'], e0.file_sha(f))
                self.assertFalse(result['integration_verified'])
                run.assert_not_called()


class InventoryTests(unittest.TestCase):
    def test_valid_inventory_only_proves_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'one.txt').write_text('fixture')
            (root/'SHA256SUMS.txt').write_text(f"{e0.file_sha(root/'one.txt')}  one.txt\n")
            result = verify_package.verify(root)
            self.assertEqual(result['package_integrity'], 'PASS')
            self.assertFalse(result['host_verified'])

    def test_extra_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'one.txt').write_text('fixture')
            (root/'SHA256SUMS.txt').write_text(f"{e0.file_sha(root/'one.txt')}  one.txt\n")
            (root/'unlisted.txt').write_text('unexpected')
            self.assertEqual(verify_package.verify(root)['package_integrity'], 'FAIL')

    def test_changed_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'one.txt').write_text('fixture')
            (root/'SHA256SUMS.txt').write_text(f"{e0.file_sha(root/'one.txt')}  one.txt\n")
            (root/'one.txt').write_text('changed')
            self.assertEqual(verify_package.verify(root)['package_integrity'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
