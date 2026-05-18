"""Hermes plugin entrypoint for chatgpt-limits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import schemas, tools

_PLUGIN_DIR = Path(__file__).parent
_HELP = (
    "Usage:\n"
    "  /chatgpt-limits           Show ChatGPT/Codex account limits\n"
    "  /chatgpt-limits json      Return raw JSON\n"
    "  /chatgpt-limits <name>    Inspect another provider supported by Hermes account_usage\n\n"
    "Examples:\n"
    "  /chatgpt-limits\n"
    "  /chatgpt-limits json\n"
    "  /chatgpt-limits anthropic\n\n"
    "CLI:\n"
    "  hermes chatgpt-limits\n"
    "  hermes chatgpt-limits --json\n"
    "  hermes chatgpt-limits anthropic"
)


def _resolve_request(arg: str, *, json_flag: bool = False) -> tuple[str, bool]:
    raw = (arg or "").strip()
    if raw in {"json", "--json"}:
        return "openai-codex", True
    provider = raw or "openai-codex"
    return provider, bool(json_flag)


def _render_result(raw_result: str, *, as_json: bool = False) -> str:
    try:
        payload = json.loads(raw_result)
    except Exception:
        return raw_result

    if as_json:
        return json.dumps(payload, indent=2, sort_keys=True)

    lines = payload.get("lines") or []
    if lines:
        return "\n".join(lines)

    error = payload.get("error") or payload.get("unavailable_reason") or "Unknown error."
    hint = payload.get("hint")
    message = [f"Unable to fetch limits: {error}"]
    if hint:
        message.append(f"Hint: {hint}")
    return "\n".join(message)


def _handle_slash(raw_args: str) -> str:
    arg = (raw_args or "").strip()
    if arg in {"help", "--help", "-h"}:
        return _HELP

    provider, as_json = _resolve_request(arg)
    return _render_result(
        tools.chatgpt_limits({"provider": provider, "markdown": True}),
        as_json=as_json,
    )


def _setup_cli_command(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "provider",
        nargs="?",
        default="openai-codex",
        help="Provider to inspect (default: openai-codex)",
    )
    subparser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Print raw JSON instead of formatted lines.",
    )


def _handle_cli_command(args) -> int:
    provider = getattr(args, "provider", "openai-codex")
    as_json = bool(getattr(args, "as_json", False))
    output = _render_result(
        tools.chatgpt_limits({"provider": provider, "markdown": False}),
        as_json=as_json,
    )
    print(output)
    return 0


def register(ctx) -> None:
    ctx.register_tool(
        name="chatgpt_limits",
        toolset="chatgpt_limits",
        schema=schemas.CHATGPT_LIMITS,
        handler=tools.chatgpt_limits,
        description="Fetch ChatGPT/OpenAI Codex account limits from the local Hermes OAuth session.",
    )
    ctx.register_command(
        "chatgpt-limits",
        handler=_handle_slash,
        description="Show ChatGPT/OpenAI Codex account limits from local OAuth.",
        args_hint="[json|provider]",
    )
    ctx.register_cli_command(
        name="chatgpt-limits",
        help="Show ChatGPT/OpenAI Codex account limits from local OAuth.",
        setup_fn=_setup_cli_command,
        handler_fn=_handle_cli_command,
        description="Query OAuth-backed ChatGPT/Codex usage from Hermes auth state.",
    )

    skills_dir = _PLUGIN_DIR / "skills"
    for child in sorted(skills_dir.iterdir() if skills_dir.exists() else []):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)
