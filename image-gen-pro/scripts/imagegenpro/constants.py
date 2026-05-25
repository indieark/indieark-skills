from __future__ import annotations

ALLOWED_PROVIDERS = ("placeholder",)
ROUTES = ("codex-cli", "api-key")
ROUTE_CHOICES = ("auto", *ROUTES)
ROUTE_PRESETS = {
    "codex-cli-first": {
        "default_route": "auto",
        "enabled_routes": ["codex-cli", "api-key"],
        "route_priority": ["codex-cli", "api-key"],
    },
    "api-key-first": {
        "default_route": "auto",
        "enabled_routes": ["api-key", "codex-cli"],
        "route_priority": ["api-key", "codex-cli"],
    },
    "codex-cli-only": {
        "default_route": "codex-cli",
        "enabled_routes": ["codex-cli"],
        "route_priority": ["codex-cli"],
    },
    "api-key-only": {
        "default_route": "api-key",
        "enabled_routes": ["api-key"],
        "route_priority": ["api-key"],
    },
}
CONFIG_KEYS = (
    "default_provider",
    "default_model",
    "output_dir",
    "run_dir",
    "batch_dir",
    "default_route",
    "enabled_routes",
    "route_priority",
    "api_key",
    "base_url",
)
NEUTRAL_REQUEST_SCHEMA = "image-gen-pro.neutral-request.v1"
PROVIDER_PAYLOAD_SCHEMA = "image-gen-pro.provider-payload.v1"
GPT_IMAGE_2_MODEL = "gpt-image-2"
NANO_BANANA_MODEL = "nano-banana-2"
MJ_MODEL = "mj"
IMAGE_MODEL_ALIASES = {
    GPT_IMAGE_2_MODEL: GPT_IMAGE_2_MODEL,
    "nano-banana": NANO_BANANA_MODEL,
    NANO_BANANA_MODEL: NANO_BANANA_MODEL,
    "nb": NANO_BANANA_MODEL,
    MJ_MODEL: MJ_MODEL,
}
IMAGE_MODEL_CHOICES = tuple(IMAGE_MODEL_ALIASES)
