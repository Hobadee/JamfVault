from __future__ import annotations

from src.classes.Script import Script
from src.classes.ScriptList import ScriptList
from pathlib import Path
import os
import json


class Disk:
    """
    Facade class for the disk file access

    All methods should take and/or return concrete classes, NOT data.
    """

    def __init__(self, path: str):
        """
        Class instatiator

        Args:
            path (str): Path to the root of the disk data
        """
        self._path = path


    def getScriptList(self) -> ScriptList:
        sl = ScriptList()
        for (dirpath, dirnames, filenames) in os.walk(self._path):
            for f in filenames:
                if f.endswith(".sh") or f.endswith(".py"):
                    sl.add(self.getScriptByPath(os.path.join(dirpath, f)))
        return sl


    def getScript(self, script: Script) -> Script:
        """
        Takes a script object, and attempts to load that script from disk

        First tactic: Take name and os.walk(self._path) for the name
        """
        if not isinstance(script.name, str):
            raise KeyError(f'Nothing to search by')

        # Set `path` here so we can error out if not found
        path = None

        # TODO: offload this search to it's own method so getScriptByPath
        # isn't requiring a search when we know where it is already.
        for (dirpath, dirnames, filenames) in os.walk(self._path):
            for f in filenames:
                if f == script.name:
                    path = os.path.join(dirpath, f)
        
        if not path:
            # File doesn't exist - we can't get it
            raise FileNotFoundError(f'Cannot find file: {script.name}')
        
        fp_s = Path(path)
        script.scriptContents = fp_s.read_text()

        # Once contents are read, check for matching JSON file, and read those contents if they exist.

        # Split the file path into directory and base name
        directory, basename = os.path.split(path)

        # Split the base name into name and extension
        name, _ = os.path.splitext(basename)

        # Create the new file name with the .json extension
        metadata = os.path.join(directory, name + '.json')

        if os.path.exists(metadata):
            # Metadata exists - read into object!
            with open(metadata, 'r') as fp_m:
                data = json.load(fp_m)
            
            # We should check each one of these before assigning
            if "info" in data:
                script.info = data["info"]
            if "notes" in data:
                script.notes = data["notes"]
            if "priority" in data:
                script.priority = data["priority"]
            if "parameter4" in data:
                script.parameter4 = data["parameter4"]
            if "parameter5" in data:
                script.parameter5 = data["parameter5"]
            if "parameter6" in data:
                script.parameter6 = data["parameter6"]
            if "parameter7" in data:
                script.parameter7 = data["parameter7"]
            if "parameter8" in data:
                script.parameter8 = data["parameter8"]
            if "parameter9" in data:
                script.parameter9 = data["parameter9"]
            if "parameter10" in data:
                script.parameter10 = data["parameter10"]
            if "parameter11" in data:
                script.parameter11 = data["parameter11"]
            if "osRequirements" in data:
                script.osRequirements = data["osRequirements"]
            if "categoryId" in data:
                try:
                    categoryId = int(data["categoryId"])
                except:
                    categoryId = None
                script.categoryId = categoryId
            if "categoryName" in data:
                script.categoryName = data["categoryName"]

        script.loadStatus = "disk"

        return script


    def getScriptByPath(self, path: str) -> Script:
        """
        Take a filename, read the file, and generate a script object from that.

        Args:
            path (str): Path of the file to get
        
        Returns:
            Script: Populated script object
        """

        s = Script()
        s.name = os.path.basename(path)

        return self.getScript(s)


    def saveScript(self, script: Script) -> Script:
        """
        Saves a new script to disk

        We save scripts to `{self._path}/scripts/{categoryName}`.  (If "categoryName" is missing,
        it will save them to the "/scripts" subdirectory).  If the user doesn't like the default
        dumping location, they can move the files around later, load operations search and match.

        Returns:
            Script: object that was saved to disk
        """

        path = os.path.join(self._path, "scripts")
        if script.categoryName:
            path = os.path.join(path, script.categoryName)
        
        os.makedirs(path, exist_ok=True)

        file = os.path.join(path, script.name)
        metadata, _ = os.path.splitext(script.name)
        metadata = os.path.join(path, f'{metadata}.json')

        fp_s = Path(file)

        fp_s.write_text(script.scriptContents)

        data = {}
        
        data["info"] = script.info
        data["notes"] = script.notes
        data["priority"] = script.priority
        data["parameter4"] = script.parameter4
        data["parameter5"] = script.parameter5
        data["parameter6"] = script.parameter6
        data["parameter7"] = script.parameter7
        data["parameter8"] = script.parameter8
        data["parameter9"] = script.parameter9
        data["parameter10"] = script.parameter10
        data["parameter11"] = script.parameter11
        data["osRequirements"] = script.osRequirements
        data["categoryId"] = script.categoryId
        data["categoryName"] = script.categoryName

        with open(metadata, 'w') as fp_m:
            json.dump(data, fp_m, ensure_ascii=False, indent = 4, sort_keys = True)

        return script
