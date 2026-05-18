"""Tool handlers for the chatgpt-limits Hermes plugin."""

from __future__ import annotations

import importlib
import json
from typing import Any


def _normalize_provider(raw: Any) -> str:
    value = str(raw or "openai-codex").strip().lower()
    aliases = {
        "chatgpt": "openai-codex",
        "codex": "openai-codex",
        "openai": "openai-codex",
        "openai-codex": "openai-codex",
    }
    return aliases.get(value, value or "openai-codex")


def _snapshot_to_dict(snapshot: Any, *, markdown: bool = False) -> dict[str, Any]:
    account_usage = importlib.import_module("agent.account_usage")
    render_account_usage_lines = getattr(account_usage, "render_account_usage_lines")

    if snapshot is None:
        return {
            "success": False,
            "available": False,
            "error": "No account-usage snapshot was returned.",
            "lines": [],
        }

    windows = []
    for window in getattr(snapshot, "windows", ()) or ():
        reset_at = getattr(window, "reset_at", None)
        windows.append(
            {
                "label": getattr(window, "label", None),
                "used_percent": getattr(window, "used_percent", None),
                "reset_at": reset_at.isoformat() if reset_at else None,
                "detail": getattr(window, "detail", None),
            }
        )

    fetched_at = getattr(snapshot, "fetched_at", None)
    return {
        "success": True,
        "available": bool(getattr(snapshot, "available", False)),
        "provider": getattr(snapshot, "provider", None),
        "source": getattr(snapshot, "source", None),
        "title": getattr(snapshot, "title", None),
        "plan": getattr(snapshot, "plan", None),
        "fetched_at": fetched_at.isoformat() if fetched_at else None,
        "windows": windows,
        "details": list(getattr(snapshot, "details", ()) or ()),
        "unavailable_reason": getattr(snapshot, "unavailable_reason", None),
        "lines": render_account_usage_lines(snapshot, markdown=markdown),
    }


def chatgpt_limits(args: dict, **kwargs) -> str:
    """Fetch account limits using Hermes' built-in OAuth-backed usage helpers."""
    del kwargs

    provider = _normalize_provider((args or {}).get("provider"))
    markdown = bool((args or {}).get("markdown", False))

    try:
        account_usage = importlib.import_module("agent.account_usage")
        fetch_account_usage = getattr(account_usage, "fetch_account_usage")
    except Exception as exc:
        return json.dumps(
            {
                "success": False,
                "available": False,
                "provider": provider,
                "error": (
                    "This plugin must run inside Hermes Agent where agent.account_usage is available. "
                    f"Import failed: {exc}"
                ),
            }
        )

    try:
        snapshot = fetch_account_usage(provider)
        payload = _snapshot_to_dict(snapshot, markdown=markdown)
        payload.setdefault("provider", provider)
        if not payload.get("available"):
            payload["hint"] = (
                "If you expected ChatGPT limits here, make sure this Hermes installation is logged in with "
                "'hermes login --provider openai-codex'."
            )
        return json.dumps(payload)
    except Exception as exc:
        return json.dumps(
            {
                "success": False,
                "available": False,
                "provider": provider,
                "error": str(exc),
                "hint": (
                    "If this is for ChatGPT/Codex, verify OAuth is set up with "
                    "'hermes login --provider openai-codex'."
                ),
            }
        )
