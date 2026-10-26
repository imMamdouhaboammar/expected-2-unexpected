#!/usr/bin/env python3
"""
verify_surgical_diff.py - Surgical diff analyzer and scope containment checker.

Evaluates a git diff or diff file for signs of scope sprawl, adjacent cosmetic edits,
unrequested abstractions, and unmanaged file blast radius.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


class DiffIssue:
    def __init__(self, category: str, message: str, file: str, line: int = 0):
        self.category = category
        self.message = message
        self.file = file
        self.line = line

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "message": self.message,
            "file": self.file,
            "line": self.line,
        }


def parse_unified_diff(diff_text: str) -> dict:
    files = {}
    current_file = None
    hunks = []
    current_hunk = []

    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            if current_file:
                if current_hunk:
                    hunks.append(current_hunk)
                    current_hunk = []
                files[current_file] = hunks
                hunks = []
            parts = line.split(" ")
            b_path = parts[-1]
            if b_path.startswith("b/"):
                current_file = b_path[2:]
            else:
                current_file = b_path
        elif line.startswith("+++ "):
            continue
        elif line.startswith("--- "):
            continue
        elif line.startswith("@@ "):
            if current_hunk:
                hunks.append(current_hunk)
                current_hunk = []
            current_hunk.append(line)
        else:
            if current_hunk is not None:
                current_hunk.append(line)

    if current_file:
        if current_hunk:
            hunks.append(current_hunk)
        files[current_file] = hunks

    return files


def analyze_diff(diff_text: str, max_files: int = 5, max_lines_added: int = 150) -> dict:
    parsed = parse_unified_diff(diff_text)
    issues: list[DiffIssue] = []

    total_added = 0
    total_deleted = 0
    file_count = len(parsed)

    if file_count > max_files:
        issues.append(
            DiffIssue(
                category="BLAST_RADIUS",
                message=f"Diff touches {file_count} files, exceeding safe threshold of {max_files}",
                file="all",
            )
        )

    for filename, hunks in parsed.items():
        file_added = 0
        file_deleted = 0

        for hunk in hunks:
            hunk_added_lines = []
            hunk_deleted_lines = []

            for line in hunk:
                if line.startswith("+") and not line.startswith("+++"):
                    total_added += 1
                    file_added += 1
                    hunk_added_lines.append(line[1:])
                elif line.startswith("-") and not line.startswith("---"):
                    total_deleted += 1
                    file_deleted += 1
                    hunk_deleted_lines.append(line[1:])

            for line in hunk_added_lines:
                # Check for speculative abstract patterns
                if re.search(r"\bclass\s+[A-Za-z0-9]+Factory\b", line):
                    issues.append(
                        DiffIssue(
                            category="SPECULATIVE_ABSTRACTION",
                            message="Added Factory pattern class; ensure explicit user request warrants this",
                            file=filename,
                        )
                    )
                if re.search(r"\b(interface|abstract class)\s+I[A-Z][A-Za-z0-9]+\b", line):
                    issues.append(
                        DiffIssue(
                            category="SPECULATIVE_ABSTRACTION",
                            message="Added abstract interface; ensure multiple implementations exist today",
                            file=filename,
                        )
                    )

            # Check for pure whitespace or comment churning
            added_stripped = [l.strip() for l in hunk_added_lines if l.strip()]
            deleted_stripped = [l.strip() for l in hunk_deleted_lines if l.strip()]
            if added_stripped == deleted_stripped and (len(hunk_added_lines) > 0 or len(hunk_deleted_lines) > 0):
                issues.append(
                    DiffIssue(
                        category="COSMETIC_CHURN",
                        message="Hunk appears to be whitespace-only reformatting",
                        file=filename,
                    )
                )

    if total_added > max_lines_added:
        issues.append(
            DiffIssue(
                category="SIZE_EXPANSION",
                message=f"Added {total_added} lines, exceeding recommended surgical threshold of {max_lines_added}",
                file="all",
            )
        )

    passed = len(issues) == 0
    return {
        "passed": passed,
        "files_touched": file_count,
        "lines_added": total_added,
        "lines_deleted": total_deleted,
        "issues": [issue.to_dict() for issue in issues],
    }


def get_git_diff(staged: bool = False, base_ref: str | None = None) -> str:
    cmd = ["git", "diff"]
    if staged:
        cmd.append("--staged")
    elif base_ref:
        cmd.append(base_ref)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return result.stdout


def run_self_tests() -> bool:
    sample_diff = """diff --git a/src/calc.py b/src/calc.py
index 123..456 100644
--- a/src/calc.py
+++ b/src/calc.py
@@ -10,3 +10,3 @@ def calc(x):
-    return x * 1
+    return x * 2
"""
    res = analyze_diff(sample_diff)
    assert res["passed"] is True, "Clean surgical diff should pass"
    assert res["lines_added"] == 1
    assert res["lines_deleted"] == 1

    bad_diff = """diff --git a/src/factory.py b/src/factory.py
index 123..456 100644
--- a/src/factory.py
+++ b/src/factory.py
@@ -1,0 +1,5 @@
+class ObjectFactory:
+    pass
"""
    res_bad = analyze_diff(bad_diff)
    assert any(i["category"] == "SPECULATIVE_ABSTRACTION" for i in res_bad["issues"]), "Should detect factory abstraction"
    return True


def main():
    parser = argparse.ArgumentParser(description="Analyze diff for surgical containment.")
    parser.add_argument("--file", type=Path, help="Path to diff file")
    parser.add_argument("--staged", action="store_true", help="Analyze staged git changes")
    parser.add_argument("--base", type=str, help="Base git commit or branch to diff against")
    parser.add_argument("--max-files", type=int, default=5, help="Max allowed files in surgical diff")
    parser.add_argument("--max-lines", type=int, default=150, help="Max added lines")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--self-test", action="store_true", help="Run internal self-tests")

    args = parser.parse_args()

    if args.self_test:
        success = run_self_tests()
        if success:
            print("[OK] Self-tests passed successfully.")
            sys.exit(0)
        sys.exit(1)

    if args.file:
        diff_text = args.file.read_text(encoding="utf-8")
    else:
        try:
            diff_text = get_git_diff(staged=args.staged, base_ref=args.base)
        except Exception as e:
            print(f"[ERROR] Failed to run git diff: {e}", file=sys.stderr)
            sys.exit(1)

    report = analyze_diff(diff_text, max_files=args.max_files, max_lines_added=args.max_lines)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status_label = "[PASS]" if report["passed"] else "[FAIL]"
        print(f"{status_label} Surgical Diff Analysis")
        print(f"Files touched: {report['files_touched']}")
        print(f"Lines added:   {report['lines_added']}")
        print(f"Lines deleted: {report['lines_deleted']}")

        if report["issues"]:
            print("\nFindings:")
            for issue in report["issues"]:
                print(f" - [{issue['category']}] {issue['message']} ({issue['file']})")

    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
