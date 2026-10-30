#!/usr/bin/env python3
"""PreToolUse hook: hard-block .env file reads/edits and Bash commands that cat/less/more .env files."""
import json, os, re, sys

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Block Read/Edit/Write on .env paths
    if tool_name in ("Read", "Edit", "Write"):
        path = tool_input.get("file_path", "") or tool_input.get("path", "")
        basename = os.path.basename(path)
        if basename in (".env",) or basename.startswith(".env."):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "block",
                    "permissionDecisionReason": f"Blocked: .env file access denied ({path})"
                }
            }))
            sys.exit(2)

    # Block Bash commands that read .env files
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        # Match: cat/less/more/head/tail/grep targeting .env (not .env.example etc in non-sensitive ways)
        dotenv_read = re.search(
            r'\b(cat|less|more|head|tail|type)\s+[^\n]*\.env\b',
            cmd
        )
        if dotenv_read:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "block",
                    "permissionDecisionReason": f"Blocked: .env read via Bash denied"
                }
            }))
            sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
