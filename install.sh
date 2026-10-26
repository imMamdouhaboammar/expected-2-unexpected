#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_NAME="expected-2-unexpected"
SKILL_SOURCE="${SCRIPT_DIR}/skills/${TARGET_NAME}"

if [ ! -d "${SKILL_SOURCE}" ]; then
  SKILL_SOURCE="${SCRIPT_DIR}"
fi

echo "📦 Installing ${TARGET_NAME} across AI agent environments..."

# 1. Claude Code
if [ -d "$HOME/.claude" ] || command -v claude >/dev/null 2>&1; then
  mkdir -p "$HOME/.claude/skills"
  rm -rf "$HOME/.claude/skills/${TARGET_NAME}"
  cp -r "${SKILL_SOURCE}" "$HOME/.claude/skills/${TARGET_NAME}"
  echo "  ✅ Installed for Claude Code -> $HOME/.claude/skills/${TARGET_NAME}"
fi

# 2. Antigravity / Gemini CLI
if [ -d "$HOME/.gemini" ]; then
  mkdir -p "$HOME/.gemini/config/skills"
  rm -rf "$HOME/.gemini/config/skills/${TARGET_NAME}"
  cp -r "${SKILL_SOURCE}" "$HOME/.gemini/config/skills/${TARGET_NAME}"
  echo "  ✅ Installed for Antigravity / Gemini CLI -> $HOME/.gemini/config/skills/${TARGET_NAME}"
fi

# 3. Codex / OpenCode
if [ -d "$HOME/.codex" ]; then
  mkdir -p "$HOME/.codex/skills"
  rm -rf "$HOME/.codex/skills/${TARGET_NAME}"
  cp -r "${SKILL_SOURCE}" "$HOME/.codex/skills/${TARGET_NAME}"
  echo "  ✅ Installed for Codex / OpenCode -> $HOME/.codex/skills/${TARGET_NAME}"
fi

# 4. Universal Agent Kernel (~/.agents/skills)
mkdir -p "$HOME/.agents/skills"
rm -rf "$HOME/.agents/skills/${TARGET_NAME}"
cp -r "${SKILL_SOURCE}" "$HOME/.agents/skills/${TARGET_NAME}"
echo "  ✅ Installed for Universal Agent Kernel -> $HOME/.agents/skills/${TARGET_NAME}"

echo ""
echo "🎉 Installation complete! The expected-2-unexpected skill is active."
