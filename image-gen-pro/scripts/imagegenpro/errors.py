class ImageGenError(Exception):
    """Base CLI error with a stable exit code."""

    def __init__(self, message: str, exit_code: int = 5) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class UsageError(ImageGenError):
    def __init__(self, message: str) -> None:
        super().__init__(message, 2)


class ConfigError(ImageGenError):
    def __init__(self, message: str) -> None:
        super().__init__(message, 3)


class RuntimeRouteError(ImageGenError):
    def __init__(self, message: str, exit_code: int = 5) -> None:
        super().__init__(message, exit_code)
