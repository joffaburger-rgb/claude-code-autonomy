#!/usr/bin/env bash
# install.sh — Claude Code Autonomy Setup installer
# Copies hook scripts to ~/.claude/hooks/ and prints merge instructions

set -e

HOOK_DIR="$HOME/.claude/hooks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Claude Code Autonomy Setup — Installer"
echo "======================================="
echo ""

# Create hooks directory
echo "Creating $HOOK_DIR ..."
mkdir -p "$HOOK_DIR"

# Copy hook scripts
echo "Copying hook scripts..."
for script in search-ground.py delegate-ground.py fix-mojibake.py verify-output.py; do
    src="$SCRIPT_DIR/hooks/$script"
    dst="$HOOK_DIR/$script"
    if [ -f "$src" ]; then
        cp "$src" "$dst"
        chmod +x "$dst"
        echo "  Copied: $dst"
    else
        echo "  WARNING: $src not found — skipping"
    fi
done

echo ""
echo "Hook scripts installed."
echo ""
echo "======================================="
echo "NEXT STEP: Merge settings-template.json"
echo "======================================="
echo ""
echo "Open ~/.claude/settings.json in a text editor and merge in the"
echo "contents of hooks/settings-template.json."
echo ""
echo "Key sections to add or merge:"
echo ""
echo "1. permissions.allow — add Bash(*), Edit(*), Write(*), Skill(*)"
echo ""
echo "2. autoMode.allow — add Bash(*) alongside \$defaults"
echo ""
echo "3. hooks — add all hook entries (SessionStart, UserPromptSubmit,"
echo "   PreToolUse, PostToolUse, PreCompact, Stop)"
echo ""
echo "If settings.json doesn't exist yet, you can copy the template directly:"
echo "  cp hooks/settings-template.json ~/.claude/settings.json"
echo ""
echo "IMPORTANT: The SessionStart hook path in settings-template.json"
echo "uses \$HOME — verify this resolves correctly in your shell."
echo "If needed, replace \$HOME with your actual home path."
echo ""
echo "======================================="
echo "AFTER INSTALL: Create memory files"
echo "======================================="
echo ""
echo "1. Create your memory directory:"
echo "   mkdir -p ~/.claude/projects/\$(basename \$HOME)/memory/"
echo ""
echo "2. Copy templates:"
echo "   cp memory/MEMORY-template.md ~/.claude/projects/\$(basename \$HOME)/memory/MEMORY.md"
echo "   cp memory/CORE-template.md ~/.claude/projects/\$(basename \$HOME)/memory/CORE.md"
echo ""
echo "3. Edit CORE.md with your details (name, role, active projects)"
echo ""
echo "4. Restart Claude Code — the SessionStart hook will load your MEMORY.md"
echo ""
echo "Done. See README.md and docs/ for full documentation."
