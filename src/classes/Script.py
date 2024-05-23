from __future__ import annotations

class Script:
    """
    
    Notes:
    - Might be good to use a "State" pattern here, with states such as "empty",
        "loaded", and "

    """

    # Do we want a way of tracking Jamf/File loaded status?
    # Perhaps loading file unloads Jamf, and visa-versa?
    # Maybe some way of checking sync between the 2?

    def __init__(self):
        self._scriptId = None
        self._name = None
        self._info = None
        self._notes = None
        self._priority = None
        self._parameter4 = None
        self._parameter5 = None
        self._parameter6 = None
        self._parameter7 = None
        self._parameter8 = None
        self._parameter9 = None
        self._parameter10 = None
        self._parameter11 = None
        self._osRequirements = None
        self._scriptContents = None
        self._categoryId = None
        self._categoryName = None

        # Not sure how I feel about these yet.  Could be useful,
        # but we aren't using them right now.
        self._loadStatus = None
        self._loadStrategy = None
        self._saveStrategy = None

    
    def from_json(self, json) -> self:
        self.scriptId = int(json["id"])
        self.name = json["name"]
        self.info = json["info"]
        self.notes = json["notes"]
        self.priority = json["priority"]
        self.parameter4 = json["parameter4"]
        self.parameter5 = json["parameter5"]
        self.parameter6 = json["parameter6"]
        self.parameter7 = json["parameter7"]
        self.parameter8 = json["parameter8"]
        self.parameter9 = json["parameter9"]
        self.parameter10 = json["parameter10"]
        self.parameter11 = json["parameter11"]
        self.osRequirements = json["osRequirements"]
        self.scriptContents = json["scriptContents"]
        self.categoryId = int(json["categoryId"])
        self.categoryName = json["categoryName"]

        self.loadStatus = "json"


    def to_json(self) -> dict:
        json = {}
        json["id"] = self.scriptId
        json["name"] = self.name
        json["info"] = self.info
        json["notes"] = self.notes
        json["priority"] = self.priority
        json["parameter4"] = self.parameter4
        json["parameter5"] = self.parameter5
        json["parameter6"] = self.parameter6
        json["parameter7"] = self.parameter7
        json["parameter8"] = self.parameter8
        json["parameter9"] = self.parameter9
        json["parameter10"] = self.parameter10
        json["parameter11"] = self.parameter11
        json["osRequirements"] = self.osRequirements
        json["scriptContents"] = self.scriptContents
        json["categoryId"] = self.categoryId
        json["categoryName"] = self.categoryName

        return json


    def __str__(self) -> str:
        return f'[{self._scriptId}] {self._name}'


    def __repr__(self) -> str:
        return f'Script({self._scriptId}, \'{self._name}\')'


    """ This implements the '|=' operator for this class

        This should function by taking list A and B, and combining them into list C, where duplicates are merged down,
        such that list C has all of items A and B, but no duplicates

        Equivelant to:
        s1 = s1 | s2 

        If s1 and s2 both have field "foo" set, the s1 data for "foo" is taken, and the s2 data is discarded
    """
    def __ior__(self, other: Script) -> Script:
        # Can we iterate all the variables?  Are there any we *woulnd't* want to iterate?
        # We may implement a "from" variable (from=Jamf) which we would want to exclude
        if not self._scriptId:
            self.scriptId = other.scriptId
        if not self._name:
            self.name = other.scriptId
        if not self._info:
            self.info = other.info
        if not self._notes:
            self.notes = other.notes
        if not self._priority:
            self.priority = other.priority
        if not self._parameter4:
            self.parameter4 = other.parameter4
        if not self._parameter5:
            self.parameter5 = other.parameter5
        if not self._parameter6:
            self.parameter6 = other.parameter6
        if not self._parameter7:
            self.parameter7 = other.parameter7
        if not self._parameter8:
            self.parameter8 = other.parameter8
        if not self._parameter9:
            self.parameter9 = other.parameter9
        if not self._parameter10:
            self.parameter10 = other.parameter10
        if not self._parameter11:
            self.parameter11 = other.parameter11
        if not self._osRequirements:
            self.osRequirements = other.osRequirements
        if not self._scriptContents:
            self.scriptContents = other.scriptContents
        if not self._categoryId:
            self.categoryId = other.categoryId
        if not self._categoryName:
            self.categoryName = other.categoryName
        
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

    # Getter and Setter for scriptId
    def get_scriptId(self) -> int:
        return self._scriptId
    def set_scriptId(self, value: int):
        if not isinstance(value, (int, type(None))):
            raise TypeError(f'ScriptId must be type "int"!')
        self._scriptId = value
    scriptId = property(get_scriptId, set_scriptId)


    # Getter and Setter for name
    def get_name(self) -> str:
        return self._name
    def set_name(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Name must be type "str"!')
        self._name = value
    name = property(get_name, set_name)


    # Getter and Setter for info
    def get_info(self) -> str:
        return self._info
    def set_info(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Info must be type "str"!')
        self._info = value
    info = property(get_info, set_info)


    # Getter and Setter for notes
    def get_notes(self) -> str:
        return self._notes
    def set_notes(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Notes must be type "str"!')
        self._notes = value
    notes = property(get_notes, set_notes)


    # Getter and Setter for priority
    # TODO: Enforce the JAMF priority ENUMs
    def get_priority(self) -> str:
        return self._priority
    def set_priority(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Priority must be type "str"!')
        self._priority = value
    priority = property(get_priority, set_priority)


    # Getter and Setter for parameter4
    def get_parameter4(self) -> str:
        return self._parameter4
    def set_parameter4(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter4 must be type "str"!')
        self._parameter4 = value
    parameter4 = property(get_parameter4, set_parameter4)


    # Getter and Setter for parameter5
    def get_parameter5(self) -> str:
        return self._parameter5
    def set_parameter5(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter5 must be type "str"!')
        self._parameter5 = value
    parameter5 = property(get_parameter5, set_parameter5)


    # Getter and Setter for parameter6
    def get_parameter6(self) -> str:
        return self._parameter6
    def set_parameter6(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter6 must be type "str"!')
        self._parameter6 = value
    parameter6 = property(get_parameter6, set_parameter6)


    # Getter and Setter for parameter7
    def get_parameter7(self) -> str:
        return self._parameter7
    def set_parameter7(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter7 must be type "str"!')
        self._parameter7 = value
    parameter7 = property(get_parameter7, set_parameter7)


    # Getter and Setter for parameter8
    def get_parameter8(self) -> str:
        return self._parameter8
    def set_parameter8(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter8 must be type "str"!')
        self._parameter8 = value
    parameter8 = property(get_parameter8, set_parameter8)


    # Getter and Setter for parameter9
    def get_parameter9(self) -> str:
        return self._parameter9
    def set_parameter9(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter9 must be type "str"!')
        self._parameter9 = value
    parameter9 = property(get_parameter9, set_parameter9)


    # Getter and Setter for parameter10
    def get_parameter10(self) -> str:
        return self._parameter10
    def set_parameter10(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter10 must be type "str"!')
        self._parameter10 = value
    parameter10 = property(get_parameter10, set_parameter10)


    # Getter and Setter for parameter11
    def get_parameter11(self) -> str:
        return self._parameter11
    def set_parameter11(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter11 must be type "str"!')
        self._parameter11 = value
    parameter11 = property(get_parameter11, set_parameter11)


    # Getter and Setter for osRequirements
    def get_osRequirements(self) -> str:
        return self._osRequirements
    def set_osRequirements(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'Parameter11 must be type "str"!')
        self._osRequirements = value
    osRequirements = property(get_osRequirements, set_osRequirements)


    # Getter and Setter for scriptContents
    def get_scriptContents(self) -> str:
        return self._scriptContents
    def set_scriptContents(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'scriptContents must be type "str"!')
        self._scriptContents = value
    scriptContents = property(get_scriptContents, set_scriptContents)


    # Getter and Setter for categoryId
    def get_categoryId(self) -> int:
        return self._categoryId
    def set_categoryId(self, value: int):
        if not isinstance(value, (int, type(None))):
            raise TypeError(f'categoryId must be type "int"!')
        self._categoryId = value
    categoryId = property(get_categoryId, set_categoryId)


    # Getter and Setter for categoryName
    def get_categoryName(self) -> str:
        return self._categoryName
    def set_categoryName(self, value: str):
        if not isinstance(value, (str, type(None))):
            raise TypeError(f'categoryName must be type "str"!')
        self._categoryName = value
    categoryName = property(get_categoryName, set_categoryName)


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
        # We need to lazy-load this.  Loading up top leads to a circular dependancy
        from src.classes.strategies.ScriptStrategies import ScriptStrategy
        if not isinstance(value, (ScriptStrategy, type(None))):
            raise TypeError(f'saveStrategy must be type "ScriptStrategy"!')
        self._saveStrategy = value
    saveStrategy = property(get_saveStrategy, set_saveStrategy)

