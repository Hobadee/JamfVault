class APIException(Exception):
    """Base class for API exceptions"""
    pass

class BadRequestException(APIException):
    """Exception for HTTP 400 Bad Request errors"""
    pass

class UnauthorizedException(APIException):
    """Exception for HTTP 401 Unauthorized errors"""
    pass

class ForbiddenException(APIException):
    """Exception for HTTP 403 Forbidden errors"""
    pass

class NotFoundException(APIException):
    """Exception for HTTP 404 Not Found errors"""
    pass

class InternalServerErrorException(APIException):
    """Exception for HTTP 500 Internal Server Error errors"""
    pass

class ServiceUnavailableException(APIException):
    """Exception for HTTP 503 Service Unavailable errors"""
    pass
