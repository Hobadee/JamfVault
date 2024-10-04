from __future__ import annotations

from abc import ABC, abstractmethod


class EaListStrategy(ABC):

    # This var should be overwritted in child classes if it's used
    # If we declare as "None" here, that should cause errors if it's used
    # but not declared
    _strategy = None

    @abstractmethod
    def load(self) -> EaList:
        """
        Abstract method to load a given EaList object.
        This method should be implemented by subclasses.

        We do *NOT* require a reference to load; we will search and load ALL available EAs
        
        Returns:
            EaList: A EaList loaded with available EAs.  EAs may be lazy-loaded
        """
        pass

    @abstractmethod
    def save(self, EaList: EaList) -> EaList:
        """
        Abstract method to save all the EAs in a given EaList object.
        EAs will be saved with the same Strategy

        This method should be implemented by subclasses.
        
        Args:
            EaList (EaList): The EaList to save

        Returns:
            EaList: A EaList loaded with available EAs.  EAs may be lazy-loaded
        """
        pass


class DummyEaListStrategy(EaListStrategy):
    """
    Dummy strategy for testing
    """

    # Static class vars
    _strategy = "dummy"

    def __init__(self, EaType: str):
        self.EaType = EaType
    
    def load(self) -> EaList:
        pass
    def save(self, EaList: EaList) -> EaList:
        pass


class DiskEaListStrategy(EaListStrategy):

    # Static class vars
    _strategy = "disk"

    def __init__(self, disk: Disk, EaType: str):
        self._disk = disk
        self.EaType = EaType

    def load(self) -> EaList:
        return self._disk.getEaList()

    def save(self, EaList: EaList) -> EaList:
        from src.factories.StrategyFactory import StrategyFactory

        strategy = StrategyFactory.EaStrategy(self._strategy, disk=self._disk)

        for ea in EaList:
            # run the FileEaStrategy on s
            strategy.save(ea)
        
        return EaList


class JamfEaListStrategy(EaListStrategy):

    # Static class vars
    _strategy = "jamf"

    def __init__(self, api: JamfApi, EaType: str):
        self._api = api
        self.EaType = EaType


    def LazyLoad(self) -> EaList:
        """
        Load *JUST* the names/IDs

        This significantly reduces API calls, but may cause
        issues down the line if you are presuming everything
        is loaded. This also breaks the "EaListsStrategy"
        contract.
        """
        eal = self._api.getEaList(self.EaType)
        return eal


    def load(self) -> EaList:
        eal = self._api.getEaList(self.EaType)
        for idx, ea in enumerate(eal):
            # TODO: CHANGEME!
            eal[idx] =  self._api.getEa(ea)
        return eal


    def save(self, EaList: EaList) -> EaList:
        from src.factories.StrategyFactory import StrategyFactory
        strategy = StrategyFactory.ScriptStrategy(self._strategy, api=self._api)
        for ea in EaList:
            strategy.save(ea)

        return EaList

