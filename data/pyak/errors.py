"""AutoKitteh SDK errors."""


class AutoKittehError(Exception):
    """Generic base class for all errors in the AutoKitteh SDK."""


class ConnectionInitError(AutoKittehError):
    """A required AutoKitteh connection was not initialized yet."""


class EnvVarError(AutoKittehError):
    """A required environment variable is missing or invalid."""


class OAuthRefreshError(AutoKittehError):
    """OAuth token refresh failed."""


class AtlassianOAuthError(AutoKittehError):
    """API calls not supported by OAuth-based Atlassian connections."""
