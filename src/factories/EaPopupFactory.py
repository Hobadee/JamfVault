from __future__ import annotations

from src.classes.EaPopup import EaPopup


class EaPopupFactory:

    @staticmethod
    def fromJson(json: str) -> EaPopup:
        """
        Returns an EaPopup object based on the passed JSON

        Returns:
            Ea: Empty Extension Attribute List object
        """
        eap = EaPopup()

        for item in json:
            eap.addChoice(item)

        return eap
