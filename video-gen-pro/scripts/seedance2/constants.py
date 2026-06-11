"""Compile-time constants and allowed value sets."""

APP_NAME = "video-gen-pro"
CLI_NAME = "videogen"
LEGACY_CLI_NAME = "seedance2"
CONFIG_FILENAME = "config.json"
DEFAULT_RUN_ROOT = "_work/seedance_upload"
DEFAULT_PROJECT_ROOT = "_work/video_projects"

DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "doubao-seedance-2-0-260128"
FAST_MODEL = "doubao-seedance-2-0-fast-260128"
DEFAULT_RATIO = "adaptive"
ALLOWED_MODELS = (DEFAULT_MODEL, FAST_MODEL)
ALLOWED_RESOLUTIONS = ("480p", "720p", "1080p")
ALLOWED_RATIOS = ("21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "adaptive")
ALLOWED_SERVICE_TIERS = ("default", "flex")
ALLOWED_TASK_STATUSES = (
    "queued", "running", "succeeded", "failed", "expired", "cancelled"
)
ALLOWED_LIST_FILTER_STATUSES = ("queued", "running", "cancelled", "succeeded", "failed")
MIN_DURATION = 4
MAX_DURATION = 15
AUTO_DURATION = -1
MIN_SEED = -1
MAX_SEED = 2**32 - 1
MIN_PAGE = 1
MAX_PAGE = 500
MAX_REFERENCE_IMAGES = 9
MAX_REFERENCE_VIDEOS = 3
MAX_REFERENCE_AUDIOS = 3
MIN_EXECUTION_EXPIRES_AFTER = 3600
MAX_EXECUTION_EXPIRES_AFTER = 259200
MAX_SAFETY_IDENTIFIER_LENGTH = 64
MAX_REQUEST_BODY_MB = 64
IMAGE_PREPARE_TARGET_MB = 8
AUDIO_PREPARE_TARGET_MB = 12
IMAGE_PREPARE_MAX_EDGE = 2048
AUDIO_PREPARE_BITRATE = "128k"

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_CONFIG = 3
EXIT_API = 4
EXIT_RUNTIME = 5

CONFIG_KEYS = (
    "api_key",
    "base_url",
    "model",
    "default_resolution",
    "default_ratio",
    "default_duration",
    "default_generate_audio",
    "default_watermark",
)
SECRET_CONFIG_KEYS: frozenset[str] = frozenset({"api_key"})

MEDIA_LIMITS_MB: dict[str, int] = {"image": 30, "video": 50, "audio": 15}
MEDIA_DEFAULTS: dict[str, str] = {
    "image": "image/png",
    "video": "video/mp4",
    "audio": "audio/mpeg",
}
SUPPORTED_IMAGE_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".heic", ".heif",
)
SUPPORTED_VIDEO_EXTENSIONS = (".mp4", ".mov")
SUPPORTED_AUDIO_EXTENSIONS = (".wav", ".mp3")
MIN_MEDIA_EDGE_PX = 300
MAX_MEDIA_EDGE_PX = 6000
MIN_MEDIA_ASPECT_RATIO = 0.4
MAX_MEDIA_ASPECT_RATIO = 2.5
MIN_REFERENCE_VIDEO_SECONDS = 2
MAX_REFERENCE_VIDEO_SECONDS = 15
MAX_REFERENCE_VIDEO_TOTAL_SECONDS = 15
MIN_REFERENCE_AUDIO_SECONDS = 2
MAX_REFERENCE_AUDIO_SECONDS = 15
MAX_REFERENCE_AUDIO_TOTAL_SECONDS = 15
MIN_REFERENCE_VIDEO_FPS = 24
MAX_REFERENCE_VIDEO_FPS = 60
MIN_REFERENCE_VIDEO_PIXELS = 640 * 640
MAX_REFERENCE_VIDEO_PIXELS = 2206 * 946
SUPPORTED_VIDEO_CODECS = ("h264", "hevc", "h265")

# GitHub distribution — override via env vars for GHE instances
# VIDEO_GEN_PRO_GITHUB_REPO  : e.g. "my-org/video-gen-pro"
# VIDEO_GEN_PRO_GITHUB_API   : e.g. "https://github.mycompany.com/api/v3" (GHE)
GITHUB_REPO = "indieark/video-gen-pro"
GITHUB_API_BASE = "https://api.github.com"
