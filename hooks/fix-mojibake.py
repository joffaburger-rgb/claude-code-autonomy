#!/usr/bin/env python3
"""PostToolUse hook: scan every written file for cp1252/Latin-1 mojibake and fix in place.

Fires after every Write or Edit tool call. If the written file contains
characters that look like cp1252 or Latin-1 bytes mis-decoded as UTF-8,
the hook re-encodes them correctly and overwrites the file silently.

Only processes text files (see TEXT_EXTS). Fails open on any error.
"""
import sys, json, os, re

TEXT_EXTS = {'.html', '.md', '.txt', '.py', '.swift', '.csv', '.js', '.ts', '.sh'}

MOJIBAKE_RE = re.compile(
    r'[\xc3][\xa2][\xe2][\x82][\xac][\xe2][\x80][\x9d]'   # â€" (em dash cp1252)
    r'|[\xc3][\xa2][\xe2][\x82][\xac][\xe2][\x80][\x98]'   # â€˜ (left single quote cp1252)
    r'|[\xc3][\xa2][\xe2][\x82][\xac][\xe2][\x80][\x99]'   # â€™ (right single quote cp1252)
    r'|[\xc3][\xa2][\xe2][\x82][\xac][\xc5][\x93]'         # â€œ (left double quote cp1252)
    r'|â€["\u009c\u009d\u0098\u0099\u0094\u0093\u0096\u0097\u0080\u0082\u0083\u0084\u0085\u0086\u0087\u0088\u0089\u008a\u008b\u008c\u008d\u008e\u008f\u0090\u0091\u0092]'
    .encode('utf-8').decode('utf-8')
)

def fix_mojibake(s):
    for enc in ('cp1252', 'latin-1'):
        try:
            fixed = s.encode(enc).decode('utf-8')
            if fixed != s:
                return fixed, enc
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return s, None

def log_file(session_id, path, fixed, enc):
    """Append file record to session verify log."""
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
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, OSError):
        return

    suspect_chars = {'â', 'Ã', ''}
    if not any(c in content for c in suspect_chars):
        log_file(session_id, path, False, None)
        return

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
