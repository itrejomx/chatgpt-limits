---
name: chatgpt-limits
description: "Use the chatgpt-limits plugin to inspect ChatGPT/OpenAI Codex OAuth-backed account limits."
version: 0.1.0
author: itrejomx + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [chatgpt, codex, oauth, limits, quota, usage, plugin]
---

# chatgpt-limits

This skill is for the `chatgpt-limits` plugin.

Use it when the user asks things like:
- check my ChatGPT limits
- show my Codex quota
- how much ChatGPT/OpenAI Codex usage is left?
- what are my session or weekly limits?

## What the plugin does

The plugin uses Hermes' built-in account-usage helpers to inspect the local user's own stored OAuth-backed provider credentials.

For ChatGPT / OpenAI Codex, it defaults to `openai-codex` and reads the local Hermes auth state. This means it can still fetch ChatGPT limits even if the active conversation is happening over another channel or even if the current model/provider is something else.

## Preferred ways to use it

1. Natural language
   - Ask the model to check ChatGPT limits.
   - If the plugin tool is available, it should call `chatgpt_limits`.

2. Explicit slash command
   - `/chatgpt-limits`
   - `/chatgpt-limits json`

## Expected output

The human-readable result should include:
- provider and plan
- session window remaining/used percentage and reset time
- weekly window remaining/used percentage and reset time
- any extra details Hermes exposes, such as credits balance

## Troubleshooting

If no limits are available:
1. Verify the plugin is installed and enabled.
2. Verify Hermes is authenticated with:
   `hermes login --provider openai-codex`
3. Start a fresh session or restart the gateway if needed.
4. Retry `/chatgpt-limits`.

## Notes

- This plugin relies on Hermes internals (`agent.account_usage`) instead of scraping the UI.
- It is intended to be lightweight and shareable as a plugin repo.
- The slash command is suitable for CLI and gateway channels like Telegram because it runs on the Hermes host and uses that machine's local auth state.
