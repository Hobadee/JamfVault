from __future__ import annotations

from src.classes.Script import Script
from src.classes.ScriptList import ScriptList
from src.factories.ScriptListFactory import ScriptListFactory
from src.factories.ScriptFactory import ScriptFactory


class TestScriptFactories:

    test_id = 1
    test_name = "TestScript"
    test_info = "Information"
    test_notes = "Long notes.  Can contains Markdown I think?\n\nCertainly newlines!"
    test_priority = "AFTER"
    test_parameter4 = "Some text describing Parameter 4"
    test_parameter5 = "Some text describing Parameter 5"
    test_parameter6 = "Some text describing Parameter 6"
    test_parameter7 = "Some text describing Parameter 7"
    test_parameter8 = "Some text describing Parameter 8"
    test_parameter9 = "Some text describing Parameter 9"
    test_parameter10 = "Some text describing Parameter 10"
    test_parameter11 = "Some text describing Parameter 11"
    test_osRequirements = "14.2"
    test_scriptContents = """#!/bin/bash\n'
                   '\n'
                   'SET_HOSTNAME(){\n'
                   '  SSN=$(/usr/sbin/system_profiler SPHardwareDataType | awk '
                   "'/Serial Number \\(system\\)/ {print $4}')\n"
                   '  # Set hostname to Serial Number\n'
                   '  /usr/sbin/scutil --set ComputerName "$SSN"\n'
                   '  /usr/sbin/scutil --set HostName "$SSN"\n'
                   '  /usr/sbin/scutil --set LocalHostName "$SSN"\n'
                   '}\n'
                   '\n'
                   'SET_HOSTNAME'"""
    test_categoryId = -1
    test_categoryName = "NONE"

    def test_basicScript(self):

        s = ScriptFactory.BasicScript(self.test_id, self.test_name)
        
        assert isinstance(s, Script)

        assert s.scriptId == self.test_id
        assert s.name == self.test_name

    def test_jamfFullScript(self):

        json = {}

        json["id"] = self.test_id
        json["name"] = self.test_name
        json["info"] = self.test_info
        json["notes"] = self.test_notes
        json["priority"] = self.test_priority
        json["parameter4"] = self.test_parameter4
        json["parameter5"] = self.test_parameter5
        json["parameter6"] = self.test_parameter6
        json["parameter7"] = self.test_parameter7
        json["parameter8"] = self.test_parameter8
        json["parameter9"] = self.test_parameter9
        json["parameter10"] = self.test_parameter10
        json["parameter11"] = self.test_parameter11
        json["osRequirements"] = self.test_osRequirements
        json["scriptContents"] = self.test_scriptContents
        json["categoryId"] = self.test_categoryId
        json["categoryName"] = self.test_categoryName

        s = ScriptFactory.JsonScript(json)

        assert isinstance(s, Script)

        assert s.scriptId == self.test_id
        assert s.name == self.test_name
        assert s.info == self.test_info
        assert s.notes == self.test_notes
        assert s.priority == self.test_priority
        assert s.parameter4 == self.test_parameter4
        assert s.parameter5 == self.test_parameter5
        assert s.parameter6 == self.test_parameter6
        assert s.parameter7 == self.test_parameter7
        assert s.parameter8 == self.test_parameter8
        assert s.parameter9 == self.test_parameter9
        assert s.parameter10 == self.test_parameter10
        assert s.parameter11 == self.test_parameter11
        assert s.osRequirements == self.test_osRequirements
        assert s.scriptContents == self.test_scriptContents
        assert s.categoryId == self.test_categoryId
        assert s.categoryName == self.test_categoryName


    def test_emptyScript(self):
        s = ScriptFactory.EmptyScript()

        assert isinstance(s, Script)

        assert not s.scriptId
        assert not s.name
        assert not s.info
        assert not s.notes
        assert not s.priority
        assert not s.parameter4
        assert not s.parameter5
        assert not s.parameter6
        assert not s.parameter7
        assert not s.parameter8
        assert not s.parameter9
        assert not s.parameter10
        assert not s.parameter11
        assert not s.osRequirements
        assert not s.scriptContents
        assert not s.categoryId
        assert not s.categoryName


    def test_emptyScripts(self):
        s = ScriptListFactory.EmptyScriptList()

        assert isinstance(s, ScriptList)

        # Unsure of exact syntax
        #assert s.length() == 0
