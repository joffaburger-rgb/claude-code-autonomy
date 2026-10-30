# HERMES TASK SPEC — push claude-code-autonomy to GitHub

## Goal
Create private GitHub repo `claude-code-autonomy` under account `joffaburger-rgb` and push the files in this directory to it.

## Files to push
All files in `~/vault/cc-autonomy-export/` (this directory):
- README.md
- install.sh
- hooks/ (settings-template.json, 4x .py scripts)
- memory/ (2x templates)
- docs/ (2x .md files)

## Steps

### Step 1 — Create the repo
Option A — gh CLI:
```bash
gh auth status  # check if authed
gh repo create claude-code-autonomy --private --description "Claude Code autonomy setup: hooks, memory system, classifier bypass" 
```

Option B — GitHub API via curl (needs GITHUB_TOKEN):
```bash
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"claude-code-autonomy","private":true,"description":"Claude Code autonomy setup: hooks, memory system, classifier bypass"}'
```

Option C — browser: navigate to github.com/new, fill in name + private, click Create.

### Step 2 — Push content
```bash
cd ~/vault/cc-autonomy-export
git init
git add -A
git commit -m "Initial commit: CC autonomy setup — hooks, memory system, classifier bypass docs"
git branch -M main
git remote add origin git@github.com:joffaburger-rgb/claude-code-autonomy.git
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519" git push -u origin main
```

### Step 3 — Report back
Confirm:
- Repo URL: https://github.com/joffaburger-rgb/claude-code-autonomy
- Visibility: private
- Files pushed: 11

## Notes
- SSH key: `~/.ssh/id_ed25519` (authed as joffaburger-rgb)
- SSH works for git push but NOT for repo creation (needs API/browser)
- If gh is already authed, Step 1 Option A is 1 command
