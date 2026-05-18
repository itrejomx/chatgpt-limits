"""Schemas for the chatgpt-limits Hermes plugin."""

CHATGPT_LIMITS = {
    "name": "chatgpt_limits",
    "description": (
        "Fetch ChatGPT / OpenAI Codex account limits from the local Hermes OAuth session. "
        "Use this when the user asks for ChatGPT, Codex, or account usage/limit status. "
        "This reads the local user's own stored OAuth credentials and can work even if the "
        "active conversation model/provider is something else."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "provider": {
                "type": "string",
                "description": (
                    "Provider to inspect. Defaults to 'openai-codex'. "
                    "Advanced use only; this plugin is mainly intended for ChatGPT/OpenAI Codex OAuth."
                ),
            },
            "markdown": {
                "type": "boolean",
                "description": "When true, render human-readable lines with markdown emphasis.",
            },
        },
        "required": [],
    },
}
