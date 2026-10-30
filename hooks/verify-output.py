#!/usr/bin/env python3
"""Stop hook: inject task verification reminder + scan written files for encoding issues."""
import json, os, sys, re

TEXT_EXTS = {'.html', '.md', '.txt', '.py', '.swift', '.csv', '.js', '.ts', '.sh'}

def check_file(path):
    issues = []
    if os.path.splitext(path)[1].lower() not in TEXT_EXTS or not os.path.isfile(path):
        return issues
    try:
        raw = open(path, 'rb').read()
    except OSError:
        return issues
    # Null bytes
    if b'\x00' in raw:
        issues.append('null bytes')
    # UTF-8 replacement char (EF BF BD)
    if b'\xef\xbf\xbd' in raw:
        issues.append('replacement chars')
    # cp1252 mojibake: em-dash (E2 80 94) misread → C3 A2 E2 82 AC E2 80 9D
    if b'\xc3\xa2\xe2\x82\xac' in raw:
        issues.append('mojibake remaining')
    # Verify readable as UTF-8
    try:
        raw.decode('utf-8')
    except UnicodeDecodeError:
        issues.append('invalid UTF-8')
    return issues

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    session_id = data.get('session_id', 'unknown')
    log_path = f"/tmp/cc-verify-{session_id}.jsonl"

    # Read + clear file log (optional — reminder fires regardless)
    file_summary = ""
    try:
        if os.path.exists(log_path):
            lines = [l.strip() for l in open(log_path) if l.strip()]
            os.remove(log_path)
            records = []
            for line in lines:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
            # Dedup
            seen = {}
            for r in records:
                seen[r.get('path', '')] = r
            records = [v for v in seen.values() if v.get('path')]

            if records:
                fixed = [r for r in records if r.get('fixed')]
                problems = []
                for r in records:
                    issues = check_file(r['path'])
                    if issues:
                        problems.append(f"{os.path.basename(r['path'])}: {', '.join(issues)}")

                parts = [f"Files written: {len(records)}"]
                if fixed:
                    parts.append(f"auto-repaired: {', '.join(os.path.basename(r['path']) for r in fixed)}")
                if problems:
                    parts.append(f"ENCODING ISSUES: {'; '.join(problems)}")
                else:
                    parts.append("encoding clean")
                file_summary = " | ".join(parts)
    except Exception:
        pass

    # Only surface if there are encoding problems — otherwise silent
    if file_summary and 'ENCODING ISSUES' in file_summary:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": f"Output check: {file_summary}"
            }
        }))

if __name__ == '__main__':
    try:
        main()
    except Exception:
        sys.exit(0)
