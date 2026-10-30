#!/usr/bin/env python3
"""Stop hook: copy session transcript to ~/.claude/logs/transcripts/ with timestamp filename."""
import json, os, shutil, sys
from datetime import datetime

LOG_DIR = os.path.expanduser("~/.claude/logs/transcripts")

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    transcript_path = data.get("transcript_path", "")
    if not transcript_path or not os.path.isfile(transcript_path):
        sys.exit(0)

    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = os.path.join(LOG_DIR, f"transcript-{ts}.json")
        shutil.copy2(transcript_path, dest)
    except Exception:
        pass

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
