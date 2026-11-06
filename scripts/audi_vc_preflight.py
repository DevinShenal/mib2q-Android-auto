#!/usr/bin/env python3
"""Read-only release preflight for Audi VC Ultimate.

This tool audits a staged package and a separately captured target-state JSON.
It has no device transport and contains no installation or restore code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "deploy/preflight/installer_contract.json"
PROFILES_PATH = ROOT / "deploy/preflight/target_profiles.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_FILE_ROOTS = (
    "/mnt/app/root/hooks",
    "/mnt/app/eso/hmi/lsd/jars",
)
ALLOWED_CONFIGS = {
    "/mnt/system/etc/eso/production/smartphone_integrator.json",
    "/mnt/system/etc/eso/production/dio_manager.json",
}


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_source(package: Path, relative: str) -> Path:
    item = PurePosixPath(relative)
    if item.is_absolute() or not item.parts or any(part in ("", ".", "..") for part in item.parts):
        raise ValueError(f"unsafe package source path: {relative!r}")
    source = package
    for part in item.parts:
        source = source / part
        if source.is_symlink():
            raise ValueError(f"symlink payload is not accepted: {relative}")
    if not source.resolve().is_relative_to(package.resolve()):
        raise ValueError(f"package source escapes package directory: {relative!r}")
    if source.is_symlink():
        raise ValueError(f"symlink payload is not accepted: {relative}")
    return source


def safe_destination(value: str) -> bool:
    p = PurePosixPath(value)
    if not p.is_absolute() or ".." in p.parts:
        return False
    if value in ALLOWED_CONFIGS:
        return True
    return any(value.startswith(root + "/") for root in ALLOWED_FILE_ROOTS)


def identity_tuple(value: dict) -> tuple:
    keys = ("platform", "vehicle_model", "head_unit_part_number", "firmware_train", "mu")
    return tuple(value.get(key) for key in keys)


def inspect_target(report: dict, registry: dict) -> list[str]:
    blockers = []
    identity = report.get("identity", {})
    keys = ("platform", "vehicle_model", "head_unit_part_number", "firmware_train", "mu")
    if any(not isinstance(identity.get(key), str) or not identity[key].strip() for key in keys):
        blockers.append("target identity is incomplete (platform/model/part/firmware/MU are required)")
        return blockers

    matches = [p for p in registry.get("profiles", [])
               if identity_tuple(p.get("identity", {})) == identity_tuple(identity)]
    if len(matches) != 1:
        blockers.append("no unique exact firmware profile exists for this target")
    else:
        profile = matches[0]
        if profile.get("status") != "validated" or profile.get("install_eligible") is not True:
            blockers.append("exact target profile is not validated for installation")
        receiver = report.get("receiver_profile", {})
        expected = profile.get("receiver_profile", {})
        for key in ("id", "gal_sha256", "receiver_sha256"):
            actual_value = receiver.get(key)
            expected_value = expected.get(key)
            if not isinstance(actual_value, str) or not SHA256_RE.fullmatch(actual_value) if key.endswith("sha256") else not actual_value:
                blockers.append(f"receiver profile field is missing or invalid: {key}")
            elif expected_value is None or actual_value != expected_value:
                blockers.append(f"receiver profile does not exactly match the validated profile: {key}")

    if report.get("evidence") != "read_only_capture":
        blockers.append("target details are not from a read-only capture")
    mod = report.get("active_mod", {})
    if not isinstance(mod, dict) or mod.get("verified") is not True:
        blockers.append("active-mod identity is unverified")
    elif not SHA256_RE.fullmatch(str(mod.get("sha256", ""))):
        blockers.append("active-mod hash is missing or invalid")

    paths = report.get("paths")
    if not isinstance(paths, dict):
        blockers.append("target path inventory is missing")
        return blockers
    return blockers


def inspect_manifest(package: Path, manifest: dict, contract: dict) -> tuple[list[str], list[str]]:
    blockers = []
    lines = []
    declared = manifest.get("artifacts")
    if not isinstance(declared, list):
        return ["release manifest must contain an artifacts array"], lines

    by_source = {}
    for item in declared:
        if not isinstance(item, dict):
            blockers.append("release manifest contains a non-object artifact entry")
            continue
        source = item.get("source")
        digest = item.get("sha256")
        if not isinstance(source, str) or source in by_source:
            blockers.append(f"invalid or duplicate release source: {source!r}")
            continue
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            blockers.append(f"missing/invalid SHA-256 in release manifest: {source}")
            continue
        by_source[source] = digest

    asset_specs = contract.get("required_assets", []) + contract.get("optional_assets", [])
    optional_groups = contract.get("optional_groups", [])
    grouped = {source for group in optional_groups for source in group.get("assets", [])}
    present_groups = {}
    for spec in asset_specs:
        source = spec["source"]
        required = spec.get("required", True)
        expected = by_source.get(source)
        try:
            path = safe_source(package, source)
        except (ValueError, OSError) as exc:
            blockers.append(str(exc))
            continue
        if not path.is_file():
            if required:
                blockers.append(f"required package file is missing: {source}")
            continue
        if expected is None:
            blockers.append(f"package file has no SHA-256 entry in release manifest: {source}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            blockers.append(f"package file hash mismatch: {source}")
            continue
        destination = spec["destination"]
        if not safe_destination(destination):
            blockers.append(f"destination is outside the allowlist: {destination}")
            continue
        lines.append(f"COPY {source} -> {destination} mode={spec['mode']} sha256={actual}")
        if source in grouped:
            for group in optional_groups:
                if source in group.get("assets", []):
                    present_groups.setdefault(group["id"], set()).add(source)

    for group in optional_groups:
        present = present_groups.get(group["id"], set())
        expected = set(group.get("assets", []))
        if present and present != expected:
            blockers.append(f"optional asset group is incomplete: {group['id']}")

    for operation in contract.get("config_changes", []):
        path = operation.get("path", "")
        if path not in ALLOWED_CONFIGS or not operation.get("backup_suffix"):
            blockers.append(f"invalid config operation or backup contract: {path}")
            continue
        lines.append(f"CONFIG {path}: {operation['operation']}; backup once as "
                     f"{path}{operation['backup_suffix']}")

    for removal in contract.get("conditional_removals", []):
        path = removal.get("path", "")
        lines.append(f"CONFLICT CHECK {path}: {removal.get('reason', 'conditional removal')}; "
                     "must be confirmed absent or this plan is blocked")
    return blockers, lines


def audit(target: dict, registry: dict, contract: dict, package: Path, manifest: dict) -> tuple[int, str]:
    target_blockers = inspect_target(target, registry)
    blockers = list(target_blockers)
    manifest_blockers, plan = inspect_manifest(package, manifest, contract)
    blockers.extend(manifest_blockers)

    paths = target.get("paths", {}) if isinstance(target.get("paths"), dict) else {}
    for spec in contract.get("required_assets", []) + contract.get("optional_assets", []):
        state = paths.get(spec["destination"])
        if not isinstance(state, dict) or state.get("state") not in ("absent", "owned_file"):
            blockers.append(f"destination state is unknown: {spec['destination']}")
        elif state["state"] == "owned_file" and not SHA256_RE.fullmatch(str(state.get("sha256", ""))):
            blockers.append(f"owned destination has no verified hash: {spec['destination']}")
        elif state["state"] == "owned_file":
            plan.append(f"REPLACE verified owned file {spec['destination']}")

    for operation in contract.get("config_changes", []):
        path = operation["path"]
        state = paths.get(path)
        if not isinstance(state, dict) or not SHA256_RE.fullmatch(str(state.get("sha256", ""))):
            blockers.append(f"config baseline hash is missing: {path}")
        backup = paths.get(path + operation["backup_suffix"])
        if not isinstance(backup, dict) or backup.get("state") not in ("absent", "verified_backup"):
            blockers.append(f"backup state is unknown: {path}{operation['backup_suffix']}")

    for removal in contract.get("conditional_removals", []):
        state = paths.get(removal["path"])
        if not isinstance(state, dict) or state.get("state") != "absent":
            blockers.append(f"unbacked deletion is not proven safe: {removal['path']}")

    lines = [
        "DRY RUN ONLY — no device connection and no files changed.",
        "Target profile: " + ("BLOCKED" if target_blockers else "MATCHED"),
        "Planned operations:",
        *(plan or ["(no package operations could be validated)"]),
        "Decision: " + ("BLOCKED" if blockers else "PREFLIGHT PASS; this is not installation authorization"),
    ]
    if blockers:
        lines.append("Blockers:")
        lines.extend(f"- {item}" for item in dict.fromkeys(blockers))
    return (2 if blockers else 0), "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", required=True,
                        help="required; this tool has no apply/install mode")
    parser.add_argument("--target-report", type=Path, required=True)
    parser.add_argument("--release-manifest", type=Path, required=True)
    parser.add_argument("--package-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        target = read_json(args.target_report)
        manifest = read_json(args.release_manifest)
        registry = read_json(PROFILES_PATH)
        contract = read_json(CONTRACT_PATH)
        code, output = audit(target, registry, contract, args.package_dir, manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PRE-FLIGHT ERROR: {exc}", file=sys.stderr)
        return 2
    print(output)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
