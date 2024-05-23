from __future__ import annotations

from abc import ABC, abstractmethod


class ScriptListStrategy(ABC):

    # This var should be overwritted in child classes if it's used
    # If we declare as "None" here, that should cause errors if it's used
    # but not declared
    _strategy = None

    @abstractmethod
    def load(self) -> ScriptList:
        """
        Abstract method to load a given ScriptList object.
        This method should be implemented by subclasses.

        We do *NOT* require a reference to load; we will search and load ALL available scripts
        
        Returns:
            ScriptList: A ScriptList loaded with available Scripts.  Scripts may be lazy-loaded
        """
        pass

    @abstractmethod
    def save(self, ScriptList: ScriptList) -> ScriptList:
        """
        Abstract method to save all the scripts in a given ScriptList object.
        Scripts will be saved with the same Strategy

        This method should be implemented by subclasses.
        
        Args:
            scriptList (ScriptList): The ScriptList to save

        Returns:
            ScriptList: A ScriptList loaded with available Scripts.  Scripts may be lazy-loaded
        """
        pass


class DummyScriptListStrategy(ScriptListStrategy):
    """
    Dummy strategy for testing
    """
    def load(self) -> ScriptList:
        pass
    def save(self, ScriptList: ScriptList) -> ScriptList:
        pass


class DiskScriptListStrategy(ScriptListStrategy):

    # Static class vars
    _strategy = "disk"

    def __init__(self, disk: Disk):
        self._disk = disk

    def load(self) -> ScriptList:
        return self._disk.getScriptList()

    def save(self, ScriptList: ScriptList) -> ScriptList:
        from src.factories.StrategyFactory import StrategyFactory

        strategy = StrategyFactory.ScriptStrategy(self._strategy, disk=self._disk)

        for s in ScriptList:
            # run the FileScriptStrategy on s
            strategy.save(s)
        
        return ScriptList


class JamfScriptListStrategy(ScriptListStrategy):

    # Static class vars
    _strategy = "jamf"

    def __init__(self, api: JamfApi):
        self._api = api


    def LazyLoad(self) -> ScriptList:
        """
        Load *JUST* the names/IDs

        This significantly reduces API calls, but may cause
        issues down the line if you are presuming everything
        is loaded. This also breaks the "ScriptListsStrategy"
        contract.
        """
        sl = self._api.getScriptList()
        return sl


    def load(self) -> ScriptList:
        sl = self._api.getScriptList()
        for idx, s in enumerate(sl):
            sl[idx] =  self._api.getScript(s)
        return sl


    def save(self, ScriptList: ScriptList) -> ScriptList:
        from src.factories.StrategyFactory import StrategyFactory
        strategy = StrategyFactory.ScriptStrategy(self._strategy, api=self._api)
        for s in ScriptList:
            strategy.save(s)

        return ScriptList

