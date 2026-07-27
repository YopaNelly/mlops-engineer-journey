class DataValidationError(Exception):
    """Raised when incoming data fails a validation check."""
    pass


class ConfigMissingError(Exception):
    """Raised when a required config value is missing."""
    pass
