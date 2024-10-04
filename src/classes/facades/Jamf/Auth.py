from __future__ import annotations

from requests.auth import HTTPBasicAuth
import requests
import time
from datetime import datetime
from src.classes.exceptions.ApiExceptions import *


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r



""" Create an Auth object for Jamf

    TODO: Renew the token BEFORE it expires.  Not sure on the best approach here on when to renew.
"""
class JamfBearerAuth(requests.auth.AuthBase):

    _token = None
    _expires = None

    _server = None
    _username = None
    _password = None

    def __init__(self, server, username, password):
        self._server = server
        self._username = username
        self._password = password

    def __call__(self, r):
        if not self.checkToken() or not self._token:
            self.getToken()
        r.headers["authorization"] = "Bearer " + self._token
        return r

    """ Get a token
    """
    def getToken(self):
        url="/api/v1/auth/token"

        rtn = requests.post(f'{self._server}{url}',
            auth=HTTPBasicAuth(self._username, self._password), headers={'Accept': 'application/json'})

        json = rtn.json()

        if hasattr(json, "httpStatus"):
            self.CheckResponse(json["httpStatus"])

        self._token = json["token"]
        # We should parse expires into a Unix timestamp or something easier to deal with
        # Returned format:
        # 2024-05-15T20:31:21.721Z
        self._expired = datetime.strptime(json["expires"], '%Y-%m-%dT%H:%M:%S.%fZ')

        return True


    """ Renew a token
    """
    def renew(self):

        # If our token is already expired, we can't renew
        if not self.checkToken():
            return self.getToken()

        url="/api/auth/keepAlive"

        rtn = requests.post(f'{self._server}{url}',
            auth=BearerAuth(self._token), headers={'Accept': 'application/json'})
        pass


    """ Checks if a token is expired or not

        Returns:
            bool: True if token is valid, false if invalid
    """
    def checkToken(self):

        # If we don't have an expiry, we aren't set - return False
        if not self._expires:
            return False

        # Jamf returns milliseconds, Python returns FLOAT seconds.
        # Multiply Python time * 1000 to match Jamf timestamps
        if(self._expires > time.time() * 1000):
            return True
        
        # Default False
        return False


    def CheckResponse(self, code):
        """
        Checks the API response and raises appropriate exceptions if there was an error

        This is duplicate code, found also in JamfApiConnection.  Can't dedup properly right now.  Dedup later.
        """
        # Anything in the 200 range is success!
        if code >= 200 and code < 300:
            return True
        
        # Handle well-known errors
        match code:
            case 400:
                raise BadRequestException("Bad request")
            case 401:
                raise UnauthorizedException("Unauthorized")
            case 403:
                raise ForbiddenException("Forbidden")
            case 404:
                raise NotFoundException("Not found")
            case 500:
                raise InternalServerErrorException("Internal server error")
            case 503:
                raise ServiceUnavailableException("Service unavailable")
            case _:
                raise APIException(f"Unexpected error: {code}")
