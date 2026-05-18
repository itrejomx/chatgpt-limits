# chatgpt-limits

A shareable Hermes plugin that exposes ChatGPT / OpenAI Codex account limits using the same internal OAuth-backed usage code Hermes already uses for `/usage`.

It is designed to be installed on another Hermes instance so the other user can authenticate with their own OAuth session and query their own limits.

## What it reuses from Hermes

Hermes already has account-limit support in `agent/account_usage.py`.

For `openai-codex`, that code:
- refreshes runtime credentials with `resolve_codex_runtime_credentials(refresh_if_expiring=True)`
- reads the stored `account_id` from Hermes auth state
- sends `Authorization: Bearer <token>`
- sends `ChatGPT-Account-Id: <account_id>` when available
- resolves the usage URL from the Codex base URL
- defaults to `https://chatgpt.com/backend-api/codex`
- queries the usage endpoint at `/wham/usage`

This plugin intentionally reuses that code instead of screen-scraping or browser automation.

## Features

- Tool: `chatgpt_limits`
- Slash command: `/chatgpt-limits`
- CLI subcommand: `hermes chatgpt-limits`
- Bundled skill: `chatgpt-limits:chatgpt-limits`
- Works from CLI and gateway chats because the command runs on the Hermes host and uses local OAuth state
- Can still fetch ChatGPT/Codex limits even when the active conversation provider is different

## Requirements

- Hermes Agent installed
- A Hermes version with plugin support
- OAuth authentication on that machine:

```bash
hermes login --provider openai-codex
```

## Install

### Option 1: install directly from GitHub

```bash
hermes plugins install https://github.com/itrejomx/chatgpt-limits.git --enable
```

After installing, start a new Hermes session. If using the gateway, restart it or start a fresh chat session so the plugin command is loaded.

### Option 2: clone locally for development

```bash
git clone https://github.com/itrejomx/chatgpt-limits.git
cd chatgpt-limits
mkdir -p ~/.hermes/plugins
ln -s "$(pwd)" ~/.hermes/plugins/chatgpt-limits
hermes plugins enable chatgpt-limits
```

## Authentication

Each user must authenticate with their own account. Tokens are not shared by this plugin.

```bash
hermes login --provider openai-codex
```

## Usage

### In any Hermes chat session

```text
/chatgpt-limits
```

### CLI command

```bash
hermes chatgpt-limits
```

### Raw JSON output

```text
/chatgpt-limits json
```

```bash
hermes chatgpt-limits --json
```

### Provider override

This plugin is mainly intended for ChatGPT / Codex, but it reuses Hermes account-usage helpers so you can optionally try another supported provider.

```text
/chatgpt-limits anthropic
```

```bash
hermes chatgpt-limits anthropic
```

## Example natural-language prompts

- check my chatgpt limits
- show my codex quota
- how much usage do I have left for chatgpt?
- show my session and weekly chatgpt limits

## Gateway / Telegram note

Yes, this can work over Telegram or other Hermes channels.

Reason: the slash command runs on the machine hosting Hermes, not on the messaging client. So it can read that Hermes instance's local OAuth state and query the same backend usage endpoint.

## Troubleshooting

If the command does not show limits:

1. Check auth:
   ```bash
   hermes login --provider openai-codex
   ```
2. Confirm the plugin is enabled:
   ```bash
   hermes plugins list
   ```
3. Start a new session or restart the gateway.
4. Try JSON mode to inspect the raw payload:
   ```bash
   hermes chatgpt-limits --json
   ```

## Files

- `plugin.yaml`
- `__init__.py`
- `schemas.py`
- `tools.py`
- `skills/chatgpt-limits/SKILL.md`

## License

MIT
