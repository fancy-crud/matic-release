class UnprocessableVersionFormat(Exception):
    """Exception raised when the version does not follow the valid semver format: x.x.x[-stage.x]
    """
    pass