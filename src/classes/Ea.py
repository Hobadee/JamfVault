from __future__ import annotations

from src.factories.EaPopupFactory import EaPopupFactory

class Ea:
    """
    
    Notes:
    - Might be good to use a "State" pattern here, with states such as "empty",
        "loaded", and "

    """

    # Do we want a way of tracking Jamf/File loaded status?
    # Perhaps loading file unloads Jamf, and visa-versa?
    # Maybe some way of checking sync between the 2?

    def __init__(self):
        self._eaId = None
        self._eaType = None
        self._name = None
        self._enabled = None
        self._description = None
        self._dataType = None
        self._inputType = None
        self._inputPlatform = None      # ONLY if type = script
        self._inputScript = None        # ONLY if type = script
        self._inventoryDisplay = None
        self._popupMenu = None

        # Not sure how I feel about these yet.  Could be useful,
        # but we aren't using them right now.
        self._loadStatus = None
        self._loadStrategy = None
        self._saveStrategy = None

    
    def from_json(self, json) -> self:
        self.eaId = int(json["id"])
        self.name = json["name"]
        self.enabled = json["enabled"]
        self.description = json["description"]
        self.dataType = json["data_type"]
        self.inputType = json["input_type"]["type"]
        self.inventoryDisplay = json["inventory_display"]

        # These may not exist - check for existence before setting
        if "platform" in json["input_type"]:
            self.inputPlatform = json["input_type"]["platform"]
        if "script" in json["input_type"]:
            self.inputScript = json["input_type"]["script"]
        if "popup_choices" in json["input_type"]:
            self.popupMenu = EaPopupFactory.fromJson(json["input_type"]["popup_choices"])

        self.loadStatus = "json"


    def to_json(self) -> dict:
        json = {}
        json["id"] = self.eaId
        json["name"] = self.name
        json["enabled"] = self.enabled
        json["description"] = self.description
        json["data_type"] = self.dataType

        json["input_type"] = {}
        json["input_type"]["type"] = self.inputType
        json["input_type"]["platform"] = self.inputPlatform
        json["input_type"]["script"] = self.inputScript

        # TODO: We aren't handling popup-menu types properly here!
        # ...we probably aren't handling other types properly either
        
        json["inventory_display"] = self.inventoryDisplay

        return json


    def __str__(self) -> str:
        return f'[{self.eaId}] {self.name}'


    def __repr__(self) -> str:
        return f'ExtensionAttribute({self.eaId}, \'{self.name}\')'


    def __ior__(self, other: ExtensionAttribute) -> ExtensionAttribute:
        """
        This implements the '|=' operator for this class

        This should function by taking list A and B, and combining them into list C, where duplicates are merged down,
        such that list C has all of items A and B, but no duplicates

        Equivelant to:
        s1 = s1 | s2 

        If s1 and s2 both have field "foo" set, the s1 data for "foo" is taken, and the s2 data is discarded.  An exception
        to this rule is the "loadStatus" and load/save strategies; loadStatus will be "merge" and if the strategies of A
        and B don't match, they will be nulled.
        """
        # First check if EA Types are the same.  If not, puke right now.
        # If both types are set, check that they match.  Puke if they don't
        if (self._eaType != None and other._eaType != None) and self._eaType != other._eaType:
            raise TypeError("Extension Attribute types don't match!  Will not merge!")

        # Can we iterate all the variables?  Are there any we *woulnd't* want to iterate?
        # We may implement a "from" variable (from=Jamf) which we would want to exclude
        if not self._eaId:
            self.eaId = other.eaId
        if not self._name:
            self.name = other.name
        if not self._enabled:
            self.enabled = other.enabled
        if not self._description:
            self.description = other.description
        if not self._dataType:
            self.dataType = other.dataType
        if not self._inputType:
            self.inputType = other.inputType
        if not self._inputPlatform:
            self.inputPlatform = other.inputPlatform
        if not self._inputScript:
            self.inputScript = other.inputScript
        if not self._inventoryDisplay:
            self.inventoryDisplay = other.inventoryDisplay
        if not self._popupMenu:
            self.popupMenu = other.popupMenu

        # Internal status
        self._loadStatus = "merge"
        if self.loadStrategy != other.loadStrategy:
            self.loadStrategy = None
        if self.saveStrategy != other.saveStrategy:
            self.saveStrategy = None

        return self


    #
    # GETTERS AND SETTERS
    #

    # Getter and Setter for eaId
    def get_eaId(self) -> int:
        return self._eaId
    def set_eaId(self, value: int):
        if not isinstance(value, (int, type(None))):
            raise TypeError(f'eaId must be type "int"!')
        self._eaId = value
    eaId = property(get_eaId, set_eaId)


    # Getter and Setter for eaType
    def get_eaType(self) -> str:
        return self._eaType
    def set_eaType(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'eaType must be type "str"!')
        self._eaType = value
    eaType = property(get_eaType, set_eaType)


    # Getter and Setter for name
    def get_name(self) -> str:
        return self._name
    def set_name(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Name must be type "str"!')
        self._name = value
    name = property(get_name, set_name)


    # Getter and Setter for enabled
    def get_enabled(self):
        return self._enabled
    def set_enabled(self, value):
        self._enabled = value
    enabled = property(get_enabled, set_enabled)


    # Getter and Setter for description
    def get_description(self) -> str:
        return self._description
    def set_description(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError('Description must be type "str"!')
        self._description = value
    description = property(get_description, set_description)


    # Getter and Setter for dataType
    def get_dataType(self):
        return self._dataType
    def set_dataType(self, value):
        self._dataType = value
    dataType = property(get_dataType, set_dataType)


    # Getter and Setter for inputType
    def get_inputType(self):
        return self._inputType
    def set_inputType(self, value):
        self._inputType = value
    inputType = property(get_inputType, set_inputType)


    # Getter and Setter for inputPlatform
    def get_inputPlatform(self):
        return self._inputPlatform
    def set_inputPlatform(self, value):
        self._inputPlatform = value
    inputPlatform = property(get_inputPlatform, set_inputPlatform)


    # Getter and Setter for inputScript
    def get_inputScript(self):
        return self._inputScript
    def set_inputScript(self, value):
        self._inputScript = value
    inputScript = property(get_inputScript, set_inputScript)


    # Getter and Setter for inventoryDisplay
    def get_inventoryDisplay(self):
        return self._inventoryDisplay
    def set_inventoryDisplay(self, value):
        self._inventoryDisplay = value
    inventoryDisplay = property(get_inventoryDisplay, set_inventoryDisplay)


    # Getter and Setter for popupMenu
    def get_popupMenu(self):
        return self._popupMenu
    def set_popupMenu(self, value):
        self._popupMenu = value
    popupMenu = property(get_popupMenu, set_popupMenu)


    # Getter and Setter for loadStatus
    def get_loadStatus(self) -> str:
        return self._loadStatus
    def set_loadStatus(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'loadStatus must be type "str"!')
        self._loadStatus = value
    loadStatus = property(get_loadStatus, set_loadStatus)


    # Getter and Setter for loadStrategy
    def get_loadStrategy(self) -> ScriptStrategy:
        return self._loadStrategy
    def set_loadStrategy(self, value):
        # We need to lazy-load this.  Loading up top leads to a circular dependancy
        from src.classes.strategies.ScriptStrategies import ScriptStrategy
        if not isinstance(value, (ScriptStrategy, type(None))):
            raise TypeError(f'loadStrategy must be type "ScriptStrategy"!')
        self._loadStrategy = value
    loadStrategy = property(get_loadStrategy, set_loadStrategy)


    # Getter and Setter for saveStrategy
    def get_saveStrategy(self) -> str:
        return self._saveStrategy
    def set_saveStrategy(self, value):
        raise NotImplementedError("Copied from Script.py - verify changes")
        # We need to lazy-load this.  Loading up top leads to a circular dependancy
        from src.classes.strategies.ScriptStrategies import ScriptStrategy
        if not isinstance(value, (ScriptStrategy, type(None))):
            raise TypeError(f'saveStrategy must be type "ScriptStrategy"!')
        self._saveStrategy = value
    saveStrategy = property(get_saveStrategy, set_saveStrategy)

