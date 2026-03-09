#!/usr/bin/env python3
"""
Daily Ansible Script Improver
This script analyzes and improves Ansible playbooks daily.

Usage:
    python3 ansible-improver.py [--platform PLATFORM] [--dry-run]

Platforms:
    - all (default)
    - cisco-asa
    - cisco-ios
    - cisco-nexus9k
    - fortigate
    - juniper-srx
    - dell-emc
"""

import os
import re
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

BASE_DIR = Path("/home/user/.openclaw/workspace")
PLATFORMS = ["cisco-asa", "cisco-ios", "cisco-nexus9k", "fortigate", "juniper-srx", "dell-emc"]

# Improvement rules
IMPROVEMENTS = {
    "idempotency": [
        (r"changed_when:\s*false", "changed_when: false  # Ensures idempotency"),
        (r"failed_when:\s*false", "failed_when: false  # Allows graceful handling"),
    ],
    "error_handling": [
        (r"(-\s*name:\s*.*\n\s*.*:\s*.*\n(?:\s+\w+:.*\n)*)", r"\1  rescue:\n    - name: Handle failure\n      debug:\n        msg: 'Task failed'"),
    ],
    "documentation": [
        (r"^---\n", r"---\n# {{ task_description }}\n# Author: Analyst (OpenClaw)\n# Last Updated: {{ date }}\n"),
    ],
}


def analyze_playbook(filepath: Path) -> Dict:
    """Analyze a single playbook and return improvement suggestions."""
    issues = []
    improvements = []
    score = 100

    with open(filepath, 'r') as f:
        content = f.read()
        lines = content.split('\n')

    # Check for best practices
    if 'changed_when' not in content:
        issues.append("Missing 'changed_when' - add for idempotency")
        score -= 10

    if 'failed_when' not in content:
        issues.append("Consider adding 'failed_when' for error handling")
        score -= 5

    if 'block:' not in content and 'tasks:' in content:
        issues.append("Consider using block/rescue for error handling")
        score -= 5

    if 'async:' not in content and len(lines) > 50:
        issues.append("Consider async for long-running tasks")
        score -= 3

    if 'register:' not in content:
        issues.append("Consider registering task output for verification")
        score -= 3

    if '# TODO' in content or '# FIXME' in content:
        issues.append("Found TODO/FIXME comments - resolve them")
        score -= 15

    if 'handler' not in content and 'save' not in content.lower():
        issues.append("Consider adding a save handler")
        score -= 5

    # Check for documentation
    if not content.strip().startswith('#'):
        improvements.append("Add documentation header at the top")
        score -= 5

    return {
        "file": str(filepath),
        "issues": issues,
        "improvements": improvements,
        "score": max(0, score),
        "lines": len(lines),
    }


def improve_playbook(filepath: Path, dry_run: bool = False) -> Tuple[bool, List[str]]:
    """Apply improvements to a playbook."""
    changes = []
    with open(filepath, 'r') as f:
        content = f.read()
        original = content

    # Add documentation header if missing
    if not content.strip().startswith('#'):
        header = f"# {filepath.stem.replace('_', ' ').title()}\n"
        header += f"# Auto-improved: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        header += "# Author: Analyst (OpenClaw)\n#\n"
        content = header + content
        changes.append("Added documentation header")

    # Ensure proper spacing
    content = re.sub(r'\n{3,}', '\n\n', content)
    if "Ensured consistent spacing" not in changes:
        changes.append("Ensured consistent spacing")

    if content != original and not dry_run:
        with open(filepath, 'w') as f:
            f.write(content)

    return content != original, changes


def scan_platform(platform: str) -> List[Dict]:
    """Scan all playbooks in a platform directory."""
    results = []
    platform_dir = BASE_DIR / platform

    if not platform_dir.exists():
        return results

    for yaml_file in platform_dir.rglob("*.yml"):
        if "group_vars" not in str(yaml_file) and "host_vars" not in str(yaml_file):
            result = analyze_playbook(yaml_file)
            results.append(result)

    return results


def generate_report(results: List[Dict], platform: str) -> str:
    """Generate a summary report."""
    report = f"\\n{'='*60}\\n"
    report += f"ANSIBLE IMPROVEMENT REPORT - {platform.upper()}\\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n"
    report += f"{'='*60}\\n\\n"

    if not results:
        report += "No playbooks found.\\n"
        return report

    total_score = sum(r['score'] for r in results) / len(results)
    total_lines = sum(r['lines'] for r in results)
    total_issues = sum(len(r['issues']) for r in results)

    report += f"📊 Summary:\\n"
    report += f"  - Total playbooks: {len(results)}\\n"
    report += f"  - Total lines: {total_lines}\\n"
    report += f"  - Average score: {total_score:.1f}/100\\n"
    report += f"  - Total issues found: {total_issues}\\n\\n"

    report += f"📁 Files Analyzed:\\n"
    for result in results:
        score_emoji = "🟢" if result['score'] >= 80 else "🟡" if result['score'] >= 60 else "🔴"
        report += f"  {score_emoji} {Path(result['file']).name}: {result['score']}/100\\n"
        if result['issues']:
            for issue in result['issues'][:3]:  # Show top 3 issues
                report += f"      ⚠️  {issue}\\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Daily Ansible Script Improver")
    parser.add_argument("--platform", choices=PLATFORMS + ["all"], default="all", help="Platform to analyze")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without making changes")
    parser.add_argument("--report-only", action="store_true", help="Only generate report, no changes")
    args = parser.parse_args()

    platforms = PLATFORMS if args.platform == "all" else [args.platform]

    for platform in platforms:
        print(f"\\n{'='*40}\\nScanning {platform}...\\n{'='*40}")

        results = scan_platform(platform)
        report = generate_report(results, platform)
        print(report)

        # Apply improvements if not dry-run or report-only
        if not args.dry_run and not args.report_only:
            playbook_dir = BASE_DIR / platform
            if playbook_dir.exists():
                for yaml_file in playbook_dir.rglob("*.yml"):
                    if "group_vars" not in str(yaml_file):
                        changed, changes = improve_playbook(yaml_file, args.dry_run)
                        if changed:
                            print(f"✅ Improved {yaml_file.name}: {', '.join(changes)}")

    # Update metrics file
    metrics_file = BASE_DIR / "network-scripts" / "metrics.json"
    metrics = {
        "last_run": datetime.now().isoformat(),
        "platforms_scanned": platforms,
        "dry_run": args.dry_run,
    }
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"\\n✅ Improver completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()