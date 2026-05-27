#!/usr/bin/env sh
#
# La Growth Machine — GTM Skills + MCP bootstrap installer
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/LaGrowthMachine/gtm-system/main/install.sh | sh
#
# Or, for the security-conscious — review before running:
#   curl -fsSL https://raw.githubusercontent.com/LaGrowthMachine/gtm-system/main/install.sh -o lgm-install.sh
#   less lgm-install.sh
#   sh lgm-install.sh
#
# What it does (in order):
#   1. Checks Node.js / npx are available.
#   2. Installs LGM GTM Skills via `npx skills add` (claude-code, cursor, codex).
#   3. Checks the user has an LGM account + collects their API key.
#      If no account → pitches LGM with a register link and exits cleanly.
#   4. Registers the LGM MCP in Claude Code via `claude mcp add --scope user
#      --transport http`, passing the API key as `Authorization: Bearer …`.
#   5. Prints suggested first-step prompts and a soft "star the repo" nudge.
#
# Honors:
#   LGM_INSTALL_NO_CLAUDE_PERMS=1  — skip the Claude MCP setup entirely.
#   LGM_INSTALL_NO_LAUNCH=1        — skip the final launch message.
#   LGM_API_KEY=...                — provide the LGM API key non-interactively.
#   LGM_INSTALL_VERBOSE=1          — show the full output of npx / claude commands
#                                    (instead of silencing it) — useful for debugging.

set -eu

SCRIPT_VERSION="2026.06.02.1"
MCP_URL="https://mcpapp.lagrowthmachine.com/mcp"
MCP_ALIAS="LaGrowthMachine"
SKILLS_PKG="LaGrowthMachine/gtm-system"

# UTM-tagged URLs — `utm_source=github` matches the repo README convention,
# `utm_medium=installer` distinguishes this entry point from the README, and
# `utm_content` identifies the specific link the user clicked.
REGISTER_URL="https://app.lagrowthmachine.com/register/?utm_source=github&utm_medium=installer&utm_campaign=gtm-system-installer&utm_content=register"
API_KEY_URL="https://app.lagrowthmachine.com/settings/integrations/api?utm_source=github&utm_medium=installer&utm_campaign=gtm-system-installer&utm_content=api-key"
REPO_URL="https://github.com/LaGrowthMachine/gtm-system"

# ─────────────────────────────────────────────────────────────────────
# Output helpers
# ─────────────────────────────────────────────────────────────────────
if [ -t 1 ]; then
  RESET="\033[0m"
  GREEN="\033[32m"
  CYAN="\033[36m"
  YELLOW="\033[33m"
  RED="\033[31m"
  GREY="\033[90m"
else
  RESET=""; GREEN=""; CYAN=""; YELLOW=""; RED=""; GREY=""
fi

say()  { printf "%b\n" "$*"; }
warn() { printf "%b\n" "${YELLOW}$*${RESET}" >&2; }
fail() { printf "%b\n" "${RED}$*${RESET}" >&2; exit 1; }

# Run a command, silencing its output unless LGM_INSTALL_VERBOSE=1.
# Keeps the happy path clean while leaving a debug escape hatch for support.
#
# stdin is redirected from /dev/null so the command can't consume the script
# itself when this installer is piped (curl ... | sh) — otherwise npx would
# swallow the rest of the script and the MCP step would never run. Interactive
# prompts read from /dev/tty directly, so they are unaffected.
run_quiet() {
  if [ "${LGM_INSTALL_VERBOSE:-0}" = "1" ]; then
    "$@" </dev/null
  else
    "$@" </dev/null >/dev/null 2>&1
  fi
}

print_logo() {
  if [ -t 1 ]; then
    say "${CYAN}"
    say "  ██╗      ██████╗ ███╗   ███╗"
    say "  ██║     ██╔════╝ ████╗ ████║"
    say "  ██║     ██║  ███╗██╔████╔██║"
    say "  ██║     ██║   ██║██║╚██╔╝██║"
    say "  ███████╗╚██████╔╝██║ ╚═╝ ██║"
    say "  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝"
    say "${RESET}"
    say "${GREY}  GTM Skills + MCP installer ${SCRIPT_VERSION}${RESET}"
    say ""
  fi
}

# Tracks whether MCP config got written (controls the final hints)
LGM_MCP_CONFIGURED=0
# Tracks the user's API key for Step 4 — collected in Step 3
LGM_API_KEY_VALUE=""

# Read input from /dev/tty when stdin is a pipe (curl | sh case).
read_tty() {
  REPLY=""
  if [ -r /dev/tty ]; then
    IFS= read -r REPLY </dev/tty || true
  else
    IFS= read -r REPLY || true
  fi
  printf "%s" "$REPLY"
}

# Read a secret silently (no echo) when possible.
read_secret_tty() {
  REPLY=""
  if [ -r /dev/tty ]; then
    if command -v stty >/dev/null 2>&1; then
      OLD_STTY="$(stty -g </dev/tty 2>/dev/null || true)"
      # If the user hits Ctrl+C while echo is off, restore it before exiting —
      # otherwise their terminal stays invisible (no echo) until they run `reset`.
      trap 'stty echo </dev/tty 2>/dev/null; printf "\n" >&2; exit 130' INT TERM
      stty -echo </dev/tty 2>/dev/null || true
      IFS= read -r REPLY </dev/tty || true
      [ -n "$OLD_STTY" ] && stty "$OLD_STTY" </dev/tty 2>/dev/null || true
      trap - INT TERM
      printf "\n" >&2
    else
      IFS= read -r REPLY </dev/tty || true
    fi
  else
    IFS= read -r REPLY || true
  fi
  printf "%s" "$REPLY"
}

# ─────────────────────────────────────────────────────────────────────
# Step 1 — check Node.js / npx
# ─────────────────────────────────────────────────────────────────────
ensure_node() {
  command -v node >/dev/null 2>&1 || fail "Node.js is required. Install from https://nodejs.org/ and re-run."
  command -v npx  >/dev/null 2>&1 || fail "npx is required (ships with Node.js ≥ 5.2). Re-install Node from https://nodejs.org/."
  say "${GREEN}✓ Node.js $(node -v) detected.${RESET}"
}

# ─────────────────────────────────────────────────────────────────────
# Step 2 — install GTM Skills (claude-code, cursor, codex)
# ─────────────────────────────────────────────────────────────────────
install_skills() {
  say "${GREY}  Installing LGM GTM Skills for claude-code, cursor, codex...${RESET}"
  if run_quiet npx --yes skills add "$SKILLS_PKG" \
       --agents claude-code cursor codex \
       --global --yes; then
    say "${GREEN}✓ LGM GTM Skills installed.${RESET}"
  else
    warn "  Skill install failed. Run manually:"
    warn "    npx skills add ${SKILLS_PKG} --agents claude-code cursor codex --global --yes"
  fi
}

# ─────────────────────────────────────────────────────────────────────
# Pitch shown to users who don't have an LGM account yet.
# Returns 0 — execution continues to the final summary; MCP config is skipped.
# ─────────────────────────────────────────────────────────────────────
pitch_lgm() {
  say ""
  say "${CYAN}La Growth Machine — what the MCP unlocks${RESET}"
  say "  ${GREEN}•${RESET} Run multichannel outbound (LinkedIn, email, voice, calls) from one workspace"
  say "  ${GREEN}•${RESET} Pull live campaign data, replies and pipeline straight into Claude"
  say "  ${GREEN}•${RESET} Push Sales Navigator audiences into LGM with one prompt"
  say "  ${GREEN}•${RESET} Native HubSpot integration — every deal mapped back to the campaign that won it"
  say ""
  say "  ${CYAN}Create your free LGM account (14-day trial):${RESET}"
  say "  ${CYAN}${REGISTER_URL}${RESET}"
  say ""
  say "  ${GREY}Once you have an account, re-run this installer and paste your API key${RESET}"
  say "  ${GREY}from ${API_KEY_URL%%\?*} to finish the setup.${RESET}"
}

# ─────────────────────────────────────────────────────────────────────
# Step 3 — check LGM account + collect the API key
#
# The LGM MCP authenticates with a Bearer token (the user's LGM API key)
# passed on every upstream call. No OAuth dance, no browser step.
#
# Behavior:
#   - LGM_INSTALL_NO_CLAUDE_PERMS=1   → skip everything, no prompt.
#   - LGM_API_KEY env var present     → non-interactive, use it directly.
#   - LGM MCP already configured      → skip (idempotent, checked via `claude mcp list`).
#   - Otherwise interactive:
#       "Do you have an LGM account?" yes → ask for API key.
#                                    no  → pitch LGM + register link, exit step.
# ─────────────────────────────────────────────────────────────────────
collect_account_and_key() {
  [ "${LGM_INSTALL_NO_CLAUDE_PERMS:-0}" = "1" ] && return 0

  # Idempotence: skip if our alias is already registered with Claude Code.
  if command -v claude >/dev/null 2>&1; then
    if claude mcp list </dev/null 2>/dev/null | grep -q "^${MCP_ALIAS}:"; then
      say "${GREEN}✓ LGM MCP already configured — skipping.${RESET}"
      LGM_MCP_CONFIGURED=1
      return 0
    fi
  fi

  # Non-interactive fast path — API key in env var.
  if [ -n "${LGM_API_KEY:-}" ]; then
    LGM_API_KEY_VALUE="$LGM_API_KEY"
    return 0
  fi

  # No TTY → can't prompt safely.
  if [ ! -t 0 ] && [ ! -r /dev/tty ]; then
    say ""
    say "${YELLOW}  No terminal detected — skipping the LGM MCP setup.${RESET}"
    say "${GREY}  Re-run interactively, or set LGM_API_KEY=... before piping to sh.${RESET}"
    return 0
  fi

  say ""
  say "${CYAN}Connect the LGM MCP?${RESET}"
  say "  The MCP lets Claude act inside your La Growth Machine workspace —"
  say "  pull campaigns, push audiences, draft replies, all from chat."
  say "  ${GREY}(an LGM account is required)${RESET}"
  say ""
  printf "  Do you already have an LGM account? [y/N]: "
  ACCOUNT_REPLY="$(read_tty)"

  case "$ACCOUNT_REPLY" in
    y|Y|yes|YES) ;;
    *)
      pitch_lgm
      return 0
      ;;
  esac

  say ""
  say "  ${CYAN}Grab your API key here:${RESET} ${API_KEY_URL}"
  say "  ${GREY}(Settings → Integrations → API)${RESET}"
  printf "  Paste your LGM API key (hidden): "
  LGM_API_KEY_VALUE="$(read_secret_tty)"

  if [ -z "$LGM_API_KEY_VALUE" ]; then
    say ""
    warn "  No API key entered — skipping MCP setup."
    warn "  Re-run when you have it: ${API_KEY_URL}"
    return 0
  fi
}

# ─────────────────────────────────────────────────────────────────────
# Step 4 — register the LGM MCP with Claude Code
#
# Uses Claude Code's native HTTP MCP transport via `claude mcp add`.
# The LGM API key is sent on every upstream call as `Authorization: Bearer <key>`.
# No mcp-remote bridge, no OAuth dance, no browser step.
# ─────────────────────────────────────────────────────────────────────
install_claude_config() {
  # Skip if Step 3 didn't collect the API key.
  [ -z "$LGM_API_KEY_VALUE" ] && return 0

  # The canonical method requires the `claude` CLI. If absent, surface the
  # one-line command the user can run later, and don't fail the installer.
  if ! command -v claude >/dev/null 2>&1; then
    say ""
    warn "  Claude Code CLI not found — can't auto-register the LGM MCP."
    warn "  Install Claude Code: https://claude.ai/download"
    warn "  Then run this once:"
    warn "    claude mcp add --scope user --transport http ${MCP_ALIAS} ${MCP_URL} --header \"Authorization:Bearer YOUR_LGM_API_KEY\""
    return 0
  fi

  # --scope user writes to ~/.claude.json (global) instead of the default
  # local scope (.mcp.json in the current dir) — so the MCP is available in
  # every project, regardless of where the installer was run from.
  if run_quiet claude mcp add --scope user --transport http "$MCP_ALIAS" "$MCP_URL" \
       --header "Authorization:Bearer $LGM_API_KEY_VALUE"; then
    say "${GREEN}✓ LGM MCP registered with Claude Code (${MCP_ALIAS}, user scope).${RESET}"
    say "${GREY}  Verify with: claude mcp list${RESET}"
    LGM_MCP_CONFIGURED=1
  else
    warn "  claude mcp add failed. Run manually:"
    warn "    claude mcp add --scope user --transport http ${MCP_ALIAS} ${MCP_URL} --header \"Authorization:Bearer YOUR_LGM_API_KEY\""
  fi
}

# ─────────────────────────────────────────────────────────────────────
# Step 5 — print first-step prompts + soft "star the repo" nudge
# ─────────────────────────────────────────────────────────────────────
print_first_steps() {
  [ "${LGM_INSTALL_NO_LAUNCH:-0}" = "1" ] && return 0

  if ! command -v claude >/dev/null 2>&1; then
    say ""
    say "${YELLOW}Claude Code not found.${RESET}"
    say "  Install: ${CYAN}https://claude.ai/download${RESET}"
    say "  Then open Claude Code and try the prompts below."
  fi

  say ""
  say "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  if [ "$LGM_MCP_CONFIGURED" = "1" ]; then
    say "${GREEN}  LGM GTM Skills + MCP ready.${RESET}"
  else
    say "${GREEN}  LGM GTM Skills installed.${RESET}"
    say "${GREY}  MCP setup skipped — re-run this installer once your LGM account is ready.${RESET}"
    say ""
    say "${CYAN}  In the meantime, the skills are ready to use.${RESET}"
    say "${GREY}    They work standalone — paste your data (deal export, campaign sequence,${RESET}"
    say "${GREY}    ICP brief…) and Claude handles the rest. Connecting the MCP later upgrades${RESET}"
    say "${GREY}    every skill to pull and push live data straight from your LGM workspace.${RESET}"
  fi
  say ""
  say "  Start with one of these prompts in Claude Code:"
  say ""
  say "  ${CYAN}Build a prospect list${RESET}"
  say "  ${GREY}→ \"Build me a Sales Navigator URL for SaaS founders in France, 50-500 employees.\"${RESET}"
  say ""
  say "  ${CYAN}Find your proven ICP${RESET}"
  say "  ${GREY}→ \"Audit my biggest closed-won deals and tell me my proven ICP.\"${RESET}"
  say ""
  say "  ${CYAN}Write a campaign${RESET}"
  say "  ${GREY}→ \"Write me a multichannel campaign for Heads of Sales at mid-market B2B SaaS.\"${RESET}"
  say ""
  say "  ${CYAN}Pressure-test a campaign before launch${RESET}"
  say "  ${GREY}→ \"Challenge this campaign before I launch it: [paste your sequence]\"${RESET}"
  say ""
  say "  ${CYAN}See which campaigns drive pipeline${RESET}"
  say "  ${GREY}→ \"Which of my campaigns is actually driving pipeline?\"${RESET}"
  say ""
  say "${GREY}  If this helped, ${RESET}${CYAN}star the repo${RESET}${GREY}: ${REPO_URL}${RESET}"
  say "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  say ""
}

# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────
print_logo
ensure_node
install_skills
collect_account_and_key
install_claude_config
print_first_steps
