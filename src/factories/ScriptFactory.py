from __future__ import annotations

from src.classes.Script import Script
from pathlib import Path
import os
import json


class ScriptFactory:


    @staticmethod
    def BasicScript(sid, name: str) -> Script:
        """
        Take a ID and Name and create an otherwise empty script object
        """
        s = Script()
        s.scriptId = sid
        s.name = name
        return s


    @staticmethod
    def JsonScript(json: dict) -> Script:
        """
        Take a full JSON script object from Jamf and create a script object here

        Args:
            json (dict): JSON Dictionary

        Returns:
            Script: Script object
        """
        s = Script()
        s.from_json(json)
        return s


    @staticmethod
    def EmptyScript() -> Script:
        """
        Returns an empty Script

        Returns:
            Script: Empty script object
        """
        s = Script()
        return s
