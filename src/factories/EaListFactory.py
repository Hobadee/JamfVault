from __future__ import annotations

from src.classes.EaList import EaList


class EaListFactory:


    @staticmethod
    def EmptyEaList() -> EaList:
        """
        Returns an empty EaList

        Returns:
            Ea: Empty Extension Attribute List object
        """
        eal = EaList()
        return eal
