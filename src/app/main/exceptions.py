"""
Problem Domain

User Defined run time Exceptions
"""


class ResourceLimitExceeded(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class UserNotFound(Exception):
    pass


class UserResourceNotFound(Exception):
    pass


class ResourceNotFound(Exception):
    pass