from __future__ import annotations

from src.classes.facades.Jamf.Auth import JamfBearerAuth
from src.classes.exceptions.ApiExceptions import *
import requests


class JamfApiConnection:
    """
    Singleton class for the Jamf API Connection

    Since we get a token good for some time, we cache that token in this singleton class.
    Whenever we need to do a new API request, we still have that token.

    Variables:
        _base_url       : Server we are connecting to
        _auth           : JamfBearerAuth object containing the authenticated session
    """

    # Global Class Vars
    _instance = None


    def __new__(cls, base_url: str, username: str, password: str):
        """
        Global class initiator
        """
        if cls._instance is None:
            cls._instance = super(JamfApiConnection, cls).__new__(cls)
            cls._instance._base_url = base_url
            cls._instance._auth = JamfBearerAuth(base_url, username, password)
        return cls._instance


    def request(self, endpoint: str, method: str = 'GET', data: dict = None):
        """ Make a Jamf API request

        TODO: Handle paginated results.

        Returns:
            response: Response object
        """
        match method:
            case "GET":
                response = requests.get(f'{self._base_url}{endpoint}',
                    auth=self._auth, headers={'Accept': 'application/json'})
            case "POST":
                response = requests.post(f'{self._base_url}{endpoint}',
                    auth=self._auth, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data = data)
            case "PUT":
                response = requests.put(f'{self._base_url}{endpoint}',
                    auth=self._auth, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data = data)
            case "DELETE":
                response = requests.delete(f'{self._base_url}{endpoint}',
                    auth=self._auth, headers={'Accept': 'application/json'})
            case _:
                raise ValueError(f"Unsupported method: {method}")
        self.CheckResponse(response)
        return response
    

    def CheckResponse(self, response):
        """
        Checks the API response and raises appropriate exceptions if there was an error
        """
        code = response.status_code

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
                raise APIException(f"Unexpected error: {response.status_code}")
