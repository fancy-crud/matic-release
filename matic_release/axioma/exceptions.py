class UnprocessableVersionFormat(Exception):
    """Exception raised when the version does not follow the valid semver format: x.x.x[-stage.x]
    """
    pass


class UnprocessableExistingTag(Exception):
    """Exception raised when the version tag already exist
    """
    pass
