#!/bin/bash
# Daily scouts, each company checked by its own AI: Codex (Luna) -> OpenAI, Grok Build -> xAI, Claude Sonnet -> Anthropic. Run by Windows task "Whats New Scouts".
cd /c/Users/lilli/AI-Shared
D=$(date +%F); SINCE=${1:-$(date -d yesterday +%F)}
P=$(cat tools/whats-new-prompt.txt)
run() { echo "$P" | sed "s/{COMPANY}/$1/g; s/{SLUG}/$2/g; s/{DATE}/$D/g; s/{SINCE}/$SINCE/g"; }
run "OpenAI (ChatGPT, Codex, ChatGPT Work)" openai | codex exec -m gpt-6-luna -s danger-full-access --skip-git-repo-check -C /c/Users/lilli/AI-Shared - > state/whats-new/.openai.log 2>&1
~/.grok/bin/grok --cwd C:/Users/lilli/AI-Shared --always-approve -m grok-4.7 -p "$(run "SpaceXAI, formerly xAI (Grok, Grok Bot, Grok Build, X Money) - check X posts from its staff too" xai)" > state/whats-new/.xai.log 2>&1
export CLAUDE_CODE_OAUTH_TOKEN="$(grep -m1 "^CLAUDE_CODE_OAUTH_TOKEN=" ~/.secrets/keys.env | cut -d= -f2-)"
run "Anthropic (Claude apps, Claude Code, Cowork, API)" anthropic | claude -p --model sonnet --dangerously-skip-permissions > state/whats-new/.anthropic.log 2>&1
