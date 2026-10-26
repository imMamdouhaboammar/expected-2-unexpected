#!/usr/bin/env python3
"""
self_check.py - Comprehensive verification runner for expected-2-unexpected skill.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def main():
    skill_dir = Path(__file__).resolve().parent.parent
    print(f"Running self-check on skill: {skill_dir.name}")

    # 1. Check SKILL.md
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.is_file(), "SKILL.md must exist"
    content = skill_md.read_text(encoding="utf-8")
    assert content.startswith("---"), "SKILL.md must start with YAML frontmatter"

    # 2. Check spec.json
    spec_json = skill_dir / "spec.json"
    assert spec_json.is_file(), "spec.json must exist"
    spec = json.loads(spec_json.read_text(encoding="utf-8"))
    assert spec.get("name") == skill_dir.name, "spec.json name must match folder"

    # 3. Check references
    ref_dir = skill_dir / "references"
    assert ref_dir.is_dir(), "references/ must exist"
    required_refs = ["heuristics.md", "surgical-diffs.md", "verification-loops.md"]
    for ref in required_refs:
        ref_file = ref_dir / ref
        assert ref_file.is_file(), f"Missing reference: {ref}"

    # 4. Check evals
    evals_json = skill_dir / "evals" / "evals.json"
    assert evals_json.is_file(), "evals/evals.json must exist"

    # 5. Check absence of personal absolute paths
    personal_path_re = re.compile(r"(/(?:Users|home)/[^\s/]+|[A-Za-z]:[/\\]+(?:Users|home)[/\\]+[^\s/\\]+)")
    for p in skill_dir.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".json", ".py", ".yaml"}:
            # Don't check self_check itself for the regex string literal
            if p.name == "self_check.py":
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            matches = personal_path_re.findall(text)
            assert not matches, f"Found personal absolute path in {p.relative_to(skill_dir)}: {matches}"

    # 6. Run verify_surgical_diff self-test
    diff_tool = skill_dir / "scripts" / "verify_surgical_diff.py"
    res = subprocess.run([sys.executable, str(diff_tool), "--self-test"], capture_output=True, text=True)
    assert res.returncode == 0, f"Diff tool self-test failed: {res.stderr}"

    print("[PASS] All structural, spec, and code integrity assertions passed.")


if __name__ == "__main__":
    main()
