from __future__ import annotations

from abc import ABC, abstractmethod

"""
TODO: Since we always need at least 2 strategies, we could put a wrapper around the strategies, and just do something like:
        EaStrategy.load(from="disk")
        EaStrategy.save(to="disk")
"""

class EaStrategy(ABC):
    """
    Abstract Strategy class for loading and saving Ea objects
    """

    @abstractmethod
    def load(self, ea: Ea) -> Ea:
        """
        Abstract method to load a given Ea object.
        This method should be implemented by subclasses.

        We require at minimum a basic Ea object to load; we can't
        load something we have no reference to

        Args:
            ea (Ea): Ea object to load
        
        Returns:
            Ea: The loaded Ea object
        """
        pass


    @abstractmethod
    def save(self, ea: Ea) -> Ea:
        """
        Abstract method to save a Ea object
        This method should be implemented by subclasses.

        This will clobber any existing matching items

        Args:
            ea (Ea): Ea object to save
        
        Returns:
            Ea: The saved Ea object
        """
        pass


class DummyEaStrategy(EaStrategy):
    """
    Dummy strategy for testing
    """
    def load(self, ea: Ea):
        pass
    def save(self, ea: Ea):
        pass


class DiskEaStrategy(EaStrategy):


    # Static class vars
    _strategy = "disk"


    def __init__(self, disk: Disk):
        self._disk = disk


    def load(self, ea: Ea) -> Ea:
        ea = self._disk.getEa(ea)
        return ea


    def save(self, ea: Ea) -> Ea:
        self._disk.saveEa(ea)
        return ea


class JamfEaStrategy(EaStrategy):
    """
    Concrete Strategy class to interface with the Jamf API

    Attributes:
        _location_type (str): Strategy being used.  We need this to chain other strategies
        _api (JamfApi): JamfApi instance to use
    """


    # Static class vars
    _strategy = "jamf"


    def __init__(self, api: JamfApi):
        """
        Class constructor

        Args:
            location_type (str): Strategy being used.  Should = "jamf"
        """
        self._api = api


    def load(self, ea: Ea) -> Ea:
        """
        Implementation of the Load method

        Attributes:
            ea (Ea): Ea object to load.  Should have a EaId

        Returns:
            Ea: The Ea object that has been loaded from Jamf
        """
        ea = self._api.getEa(ea)
        return ea


    def save(self, ea: Ea) -> Ea:
        return self._api.saveEa(ea)

