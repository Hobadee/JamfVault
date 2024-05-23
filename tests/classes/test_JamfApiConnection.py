from __future__ import annotations

from src.classes.facades.Jamf.JamfApiConnection import JamfApiConnection
import os

class TestJamfApiConnection:


    """ Test that we are a true singleton class
    """
    def test_Singleton(self):
        if "JAMF_USERNAME" in os.environ and "JAMF_PASSWORD" in os.environ and "JAMF_SERVER" in os.environ:
            server   = os.environ["JAMF_SERVER"]    # "https://myserver.jamfcloud.com"
            username = os.environ["JAMF_USERNAME"]
            password = os.environ["JAMF_PASSWORD"]
        else:
            # We don't have username or password set - we can't test
            raise Exception("Jamf username or password not set - cannot test!")
            return True

        base_url = server

        con1 = JamfApiConnection(base_url, username, password)
        con2 = JamfApiConnection(base_url, username, password)

        assert con1 == con2

        # TODO: We should also be able to effect con1 and have con2 reflect those changes.  Attempt that here
