from __future__ import annotations

from src.factories.ScriptFactory import ScriptFactory
from src.factories.ScriptListFactory import ScriptListFactory
from src.factories.EaFactory import EaFactory
from src.factories.EaListFactory import EaListFactory
#from src.classes.Ea import Ea
#from src.classes.EaList import EaList
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

        script = self.getScript(script)
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


    #
    # Extension Attribute Functions
    #

    def getEaList(self, EaType: str) -> EaList:
        """
        Gets a list of Extension Attributes
        Figures out if we want Computer, Mobile, or User EAs based on passed variable

        This is a lazy-loader

        Args:
            EaType (str): Type of EA - "computer", "mobile", or "user"
        
        Returns:
            ExtensionAttributeList: ExtensionAttribute list object
        """

        match EaType:
            case "computer":
                return self.getCeaList()
            case "mobile":
                return self.getMeaList()
            case "user":
                return self.getMeaList()
            case _:
                raise ValueError(f"Unknown EA type: {EaType}")
        raise RuntimeError("Something went very wrong.  We shouldn't be here.")

    
    def getCeaList(self) -> EaList:
        """
        Gets a list of Computer Extension Attributes

        This is a lazy-loader
        
        Returns:
            ExtensionAttributeList: ExtensionAttribute list object
        """
        endpoint = f"/JSSResource/computerextensionattributes"
        key = "computer_extension_attributes"
        eaType = "computer"
        return self._getEaList(endpoint=endpoint, key=key, eaType=eaType)
    
    def getMeaList(self) -> EaList:
        """
        Gets a list of Mobile Device Extension Attributes

        This is a lazy-loader
        
        Returns:
            ExtensionAttributeList: ExtensionAttribute list object
        """
        endpoint = f"/JSSResource/mobiledeviceextensionattributes"
        key = "mobile_device_extension_attributes"
        eaType = "mobile"
        return self._getEaList(endpoint=endpoint, key=key, eaType=eaType)

    def getUeaList(self) -> EaList:
        """
        Gets a list of User Extension Attributes

        This is a lazy-loader

        Returns:
            ExtensionAttributeList: ExtensionAttribute list object
        """
        endpoint = f"/JSSResource/userextensionattributes"
        key = "user_extension_attributes"
        eaType = "user"
        return self._getEaList(endpoint=endpoint, key=key, eaType=eaType)
    
    def _getEaList(self, endpoint: str, key: str, eaType: str) -> EaList:
        """
        Gets a list of Extension Attributes.  Can be either Computer, Mobile Device, or
        user, depending on correct endpoint and key.

        This is a lazy-loader

        Args:
            endpoint (str): API endpoint to hit
            key (str): Results are wrapped in a dict key.  What is that key?
            eaType (str): Type of EA List this is.  Should probably be an ENUM later

        Returns:
            ExtensionAttributeList: ExtensionAttribute list object
        """
        method = 'GET'
        response = self._JAC.request(endpoint, method)

        EaList = EaListFactory.EmptyEaList()

        for item in response.json()[key]:
            ea = EaFactory.BasicEa(eaid=item["id"], name=item["name"])
            if hasattr(item, "enabled"):
                ea.enabled = item["enabled"]
            ea.eaType = eaType
            EaList.add(ea)

        return EaList


    def getEa(self, Ea: Ea) -> Ea:
        """
        Gets a single Extension Attribute, by Ea reference

        We should preserve the passed "Ea" reference here
        so that we update it, rather than creating a new object

        Args:
            Ea (Ea): Extension Attribute object to get from Jamf

        Returns:
            Ea: Extension Attribute object
        """
        if not isinstance(Ea.eaId, int):
            raise ValueError()
    
        match Ea.eaType:
            case "computer":
                endpoint = f"/JSSResource/computerextensionattributes/id/{Ea.eaId}"
                key = "computer_extension_attribute"
            case "mobile":
                endpoint = f"/JSSResource/mobiledeviceextensionattributes/id/{Ea.eaId}"
                # FIXME: WRONG KEY!
                key = "computer_extension_attribute"
            case "user":
                # endpoint = f"/JSSResource/userextensionattributes/name/{Ea.name}"
                endpoint = f"/JSSResource/userextensionattributes/id/{Ea.eaId}"
                # FIXME: WRONG KEY!
                key = "computer_extension_attribute"
            case _:
                raise ValueError(f"{Ea.eaType} isn't a valid type of Extension Attribute")
            
        method = 'GET'
        response = self._JAC.request(endpoint, method)

        Ea.from_json(response.json()[key])
        Ea.loadStatus = "jamf"

        return Ea
    

    def getEaById(self, eaId: int, eaType: str) -> Ea:
        """
        Gets a single Extension Attribute of Type, by ID

        Args:
            eaId (int): ID of the Jamf Extension Attribute to get
            eaType (str): Type of EA to get.  (May be ENUM in future)

        Returns:
            Ea: Extension Attribute object
        """
        ea = EaFactory.EmptyEa()
        ea.eaId = eaId

        ea = self.getEa(ea)
        return ea
    

    def saveEa(self, Ea: Ea) -> Ea:
        """
        If an EA has an ID, update that ID, otherwise create a new script

        Should we try to match on name at all?

        Args:
            EaId (ExtensionAttribute): object to be updated or saved in Jamf
        
        Returns:
            ExtensionAttribute: object that was saved to Jamf
        """
        raise NotImplementedError("JamfApi.saveEa not implemented yet!")
    
    def createEa(self) -> Ea:
        raise NotImplementedError("JamfApi.createEa not implemented yet!")
    
    def updateEa(self) -> Ea:
        raise NotImplementedError("JamfApi.updateEa not implemented yet!")
