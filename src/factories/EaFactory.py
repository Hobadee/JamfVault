from __future__ import annotations

from src.classes.Ea import Ea


class EaFactory:


    @staticmethod
    def BasicEa(eaid, name: str) -> Ea:
        """
        Take a ID and Name and create an otherwise empty ea object
        """
        ea = Ea()
        ea.eaId = eaid
        ea.name = name
        return ea


    @staticmethod
    def JsonEa(json: dict) -> Ea:
        """
        Take a full JSON ea object from Jamf and create a ea object here

        Args:
            json (dict): JSON Dictionary

        Returns:
            Ea: Ea object
        """
        ea = Ea()
        ea.from_json(json)
        return ea


    @staticmethod
    def EmptyEa() -> Ea:
        """
        Returns an empty Ea

        Returns:
            Ea: Empty Extension Attribute object
        """
        ea = Ea()
        return ea
