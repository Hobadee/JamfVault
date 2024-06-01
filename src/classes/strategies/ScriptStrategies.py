from __future__ import annotations

from abc import ABC, abstractmethod

"""
TODO: Since we always need at least 2 strategies, we could put a wrapper around the strategies, and just do something like:
        ScriptStrategy.load(from="disk")
        ScriptStrategy.save(to="disk")
"""

class ScriptStrategy(ABC):
    """
    Abstract Strategy class for loading and saving Script objects
    """

    @abstractmethod
    def load(self, script: Script) -> Script:
        """
        Abstract method to load a given Script object.
        This method should be implemented by subclasses.

        We require at minimum a basic script object to load; we can't
        load something we have no reference to

        Args:
            script (Script): Script object to load
        
        Returns:
            Script: The loaded script object
        """
        pass


    @abstractmethod
    def save(self, script: Script) -> Script:
        """
        Abstract method to save a Script object
        This method should be implemented by subclasses.

        This will clobber any existing matching items

        Args:
            script (Script): Script object to save
        
        Returns:
            Script: The saved script object
        """
        pass


class DummyScriptStrategy(ScriptStrategy):
    """
    Dummy strategy for testing
    """

    # Static class vars
    _strategy = "dummy"

    def load(self, script: Script):
        pass
    def save(self, script: Script):
        pass


class DiskScriptStrategy(ScriptStrategy):
    """
    Concrete Strategy class to interface with files on disk

    Attributes:
        _strategy (str): Strategy being used.  We need this to chain other strategies
        _disk (Disk): Disk instance to use
    """


    # Static class vars
    _strategy = "disk"


    def __init__(self, disk: Disk):
        """
        Class constructor

        Args:
            disk (Disk): Disk facade instance being used
        """
        self._disk = disk


    def load(self, script: Script) -> Script:
        script = self._disk.getScript(script)
        return script


    def save(self, script: Script) -> Script:
        self._disk.saveScript(script)
        return script


class JamfScriptStrategy(ScriptStrategy):
    """
    Concrete Strategy class to interface with the Jamf API

    Attributes:
        _strategy (str): Strategy being used.  We need this to chain other strategies
        _api (JamfApi): JamfApi instance to use
    """


    # Static class vars
    _strategy = "jamf"


    def __init__(self, api: JamfApi):
        """
        Class constructor

        Args:
            api (JamfApi): JamfApi facade instance being used
        """
        self._api = api


    def load(self, script: Script) -> Script:
        """
        Implementation of the Load method

        Attributes:
            script (Script): Script object to load.  Should have a ScriptId

        Returns:
            Script: The script object that has been loaded from Jamf
        """
        script = self._api.getScript(script)
        return script


    def save(self, script: Script) -> Script:
        """
        Implementation of the Save method

        Attributes:
            script (Script): Script object to save.

        Returns:
            Script: The script object that has been saved to Jamf.  This may either be the original object (if updated) or a new object (if created)
        """
        return self._api.saveScript(script)

