#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("audi_vc_preflight", ROOT / "scripts/audi_vc_preflight.py")
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)

class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.package = Path(self.tmp.name) / "package"
        self.package.mkdir()
        contract = json.loads((ROOT / "deploy/preflight/installer_contract.json").read_text())
        self.contract = contract
        self.target = json.loads((ROOT / "deploy/preflight/examples/a5-owner-report.example.json").read_text())
        self.registry = json.loads((ROOT / "deploy/preflight/target_profiles.json").read_text())
        self.manifest = {"artifacts": []}
        for spec in contract["required_assets"]:
            data = ("synthetic:" + spec["source"]).encode()
            (self.package / spec["source"]).write_bytes(data)
            self.manifest["artifacts"].append({"source": spec["source"], "sha256": hashlib.sha256(data).hexdigest()})

    def test_owner_report_fails_closed_and_dry_run_does_not_write(self):
        before = {p.name: p.read_bytes() for p in self.package.iterdir()}
        code, output = preflight.audit(self.target, self.registry, self.contract, self.package, self.manifest)
        self.assertEqual(code, 2)
        self.assertIn("exact target profile is not validated", output)
        self.assertIn("active-mod identity is unverified", output)
        self.assertIn("no device connection and no files changed", output)
        self.assertIn("CONFIG /mnt/system/etc/eso/production/smartphone_integrator.json", output)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.package.iterdir()})

    def test_unknown_firmware_is_blocked(self):
        target = json.loads(json.dumps(self.target))
        target["identity"]["mu"] = "MU9999"
        code, output = preflight.audit(target, self.registry, self.contract, self.package, self.manifest)
        self.assertEqual(code, 2)
        self.assertIn("no unique exact firmware profile", output)

    def test_malformed_receiver_report_is_blocked_without_crashing(self):
        target = json.loads(json.dumps(self.target))
        target["receiver_profile"] = None
        code, output = preflight.audit(target, self.registry, self.contract, self.package, self.manifest)
        self.assertEqual(code, 2)
        self.assertIn("receiver profile evidence is missing or malformed", output)

    def test_hash_mismatch_is_blocked(self):
        manifest = json.loads(json.dumps(self.manifest))
        manifest["artifacts"][0]["sha256"] = "0" * 64
        code, output = preflight.audit(self.target, self.registry, self.contract, self.package, manifest)
        self.assertEqual(code, 2)
        self.assertIn("package file hash mismatch", output)

    def test_path_traversal_is_blocked(self):
        contract = json.loads(json.dumps(self.contract))
        contract["required_assets"][0]["source"] = "../outside.bin"
        code, output = preflight.audit(self.target, self.registry, contract, self.package, self.manifest)
        self.assertEqual(code, 2)
        self.assertIn("unsafe package source path", output)

if __name__ == "__main__":
    unittest.main()
