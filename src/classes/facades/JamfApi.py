from __future__ import annotations

from src.factories.ScriptFactory import ScriptFactory
from src.factories.ScriptListFactory import ScriptListFactory
import datetime
import json


class JamfApi:
    """
    Facade class for the Jamf API

    All methods should take and/or return concrete classes, NOT data.
    """

    def __init__(self, ApiConnection: JamfApiConnection):
        self._JAC = ApiConnection


    def getScriptList(self) -> ScriptList:
        """
        Gets a list of all scripts currently in Jamf and their IDs

        Returns:
            ScriptList: ScriptList object with basic (non-populated!) script objects
        """
        endpoint = "/JSSResource/scripts"
        method = 'GET'
        response = self._JAC.request(endpoint, method)

        scripts = ScriptListFactory.EmptyScriptList()

        for s in response.json()["scripts"]:
            script = ScriptFactory.BasicScript(sid=s["id"], name=s["name"])
            script.loadStatus = "lazy"
            scripts.add(script)

        return scripts


    def getScript(self, script: Script) -> Script:
        """
        Gets a single script, by script reference

        We should preserve the passed "script" reference here
        so that we update it, rather than creating a new object

        Args:
            script (Script): Script object to get from Jamf

        Returns:
            Script: script object
        """
        if not isinstance(script.scriptId, int):
            raise ValueError()

        endpoint = f"/api/v1/scripts/{script.scriptId}"
        method = 'GET'
        response = self._JAC.request(endpoint, method)

        script.from_json(response.json())
        script.loadStatus = "jamf"

        return script


    def getScriptById(self, scriptId: int) -> Script:
        """
        Gets a single script, by ID

        Args:
            id (int): ID of the Jamf script to get

        Returns:
            Script: script object
        """
        script = ScriptFactory.EmptyScript()
        script.scriptId = scriptId

        return self.getScript(script)
        return script


    def saveScript(self, script: Script) -> Script:
        """
        If a script has an ID, update that ID, otherwise create a new script

        Should we try to match on name at all?

        Args:
            script (Script): object to be updated or saved in Jamf
        
        Returns:
            Script: object that was saved to Jamf
        """
        if script.scriptId:
            return self.updateScript(script)

        elif script.name:
            # Check if there is a matching name in Jamf first
            sl = self.getScriptList()
            if sl.ExistsByName(script.name):
                s = sl.GetByName(script.name)
                script.scriptId = s.scriptId
                return self.updateScript(script)

        return self.createScript(script)


    def updateScript(self, script: Script) -> Script:
        """
        Updates a single script

        Returns:
            Script: object that was updated
        """

        if not script.scriptId:
            raise ValueError()

        endpoint = f"/api/v1/scripts/{script.scriptId}"
        method = 'PUT'
        payload = json.dumps(script.to_json())
        response = self._JAC.request(endpoint, method, data=payload)

        self.postScriptHistory(script, f'Updated via sync script at {datetime.datetime.now()}')

        return script


    def createScript(self, script: Script) -> Script:
        """
        Posts a new script to Jamf

        Create a Script in Jamf

        Returns:
            Script: object that was saved to Jamf
        """

        endpoint = f"/api/v1/scripts"
        method = 'POST'
        payload = json.dumps(script.to_json())
        response = self._JAC.request(endpoint, method, data=payload)
        
        scriptId = int(response.json()["id"])
        script.scriptId = scriptId

        self.postScriptHistory(script, "Initial version from sync")
        
        return script


    def postScriptHistory(self, script: Script, note: str) -> Script:
        """
        Posts a new Script History note to Jamf
        """

        # I'm not entirely sure this is working.  It should be, but I got a 400 error
        # when trying it out.  I'm going to disable this for now.
        return script

        ### METHOD DISABLED ###
        if not isinstance(script.scriptId, int):
            raise ValueError()

        scriptId = script.scriptId

        endpoint = f"/api/v1/scripts/{scriptId}/history"
        method = 'POST'
        response = self._JAC.request(endpoint, method)

