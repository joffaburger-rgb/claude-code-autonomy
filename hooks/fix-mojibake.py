#!/usr/bin/env python3
"""PostToolUse hook: scan every written file for cp1252/Latin-1 mojibake and fix in place.

Detection uses byte-pattern matching only — safe for UTF-8, CJK, Japanese, Arabic, emoji.
Never triggers on clean UTF-8 files that happen to contain Latin characters.
"""
import sys, json, os

TEXT_EXTS = {'.html', '.md', '.txt', '.py', '.swift', '.csv', '.js', '.ts', '.sh'}

# Known mojibake byte signatures: cp1252 characters misread as UTF-8.
# Each tuple is a (bytes_pattern, description).
# These byte sequences cannot appear in valid UTF-8 text.
MOJIBAKE_SIGNATURES = [
    b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d',  # â€" em dash
    b'\xc3\xa2\xe2\x82\xac\xe2\x80\x98',  # â€˜ left single quote
    b'\xc3\xa2\xe2\x82\xac\xe2\x80\x99',  # â€™ right single quote
    b'\xc3\xa2\xe2\x82\xac\xc5\x93',       # â€œ left double quote
    b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9c',  # â€œ left double quote variant
    b'\xc3\x83\xc2\xa9',                    # Ã© → é
    b'\xc3\x83\xc2\xa0',                    # Ã  → à
    b'\xc3\x83\xc2\xa8',                    # Ã¨ → è
    b'\xc3\x83\xc2\xbc',                    # Ã¼ → ü
    b'\xc3\x83\xc2\xb6',                    # Ã¶ → ö
    b'\xc3\x83\xc2\xa4',                    # Ã¤ → ä
]

def has_mojibake_bytes(raw: bytes) -> bool:
    return any(sig in raw for sig in MOJIBAKE_SIGNATURES)

def fix_mojibake(s: str):
    for enc in ('cp1252', 'latin-1'):
        try:
            fixed = s.encode(enc).decode('utf-8')
            if fixed != s:
                return fixed, enc
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return s, None

def log_file(session_id, path, fixed, enc):
    try:
        log = f"/tmp/cc-verify-{session_id}.jsonl"
        with open(log, 'a') as f:
            f.write(json.dumps({"path": path, "fixed": fixed, "enc": enc}) + "\n")
    except Exception:
        pass

def scan_and_fix(path, session_id):
    ext = os.path.splitext(path)[1].lower()
    if ext not in TEXT_EXTS:
        return
    if not os.path.isfile(path):
        return

    # Read as bytes first — safe detection, no risk of corruption
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except OSError:
        return

    # Only proceed if known mojibake byte patterns are present
    if not has_mojibake_bytes(raw):
        log_file(session_id, path, False, None)
        return

    # Decode as UTF-8 to get string for fix attempt
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        return  # Not valid UTF-8 — skip

    fixed, enc = fix_mojibake(content)
    if enc and fixed != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        log_file(session_id, path, True, enc)
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"[mojibake-fix] repaired {os.path.basename(path)} ({enc} misread)"
            }
        }))
    else:
        log_file(session_id, path, False, None)

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    session_id = data.get('session_id', 'unknown')
    path = (data.get('tool_input') or {}).get('file_path') or \
           (data.get('tool_response') or {}).get('filePath')
    if path:
        scan_and_fix(path, session_id)

if __name__ == '__main__':
    main()
