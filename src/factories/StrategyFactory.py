from __future__ import annotations

from src.classes.strategies.ScriptStrategies import DiskScriptStrategy, JamfScriptStrategy
from src.classes.strategies.ScriptListStrategies import DiskScriptListStrategy, JamfScriptListStrategy

from src.classes.strategies.EaStrategies import DiskEaStrategy, JamfEaStrategy
from src.classes.strategies.EaListStrategies import DiskEaListStrategy, JamfEaListStrategy


class StrategyFactory:
    @staticmethod
    def ScriptStrategy(location_type: str, **kwargs) -> ScriptStrategy:
        """
        Create a Script strategy object for a given "location_type"

        Args:
            location_type (str): String representation of the location type.  Currently "disk" or "jamf"
        
        Returns:
            ScriptStrategy: Concrete implementation of ScriptStrategy
        """
        match location_type:
            case "disk":
                disk = kwargs.get('disk')
                if not disk:
                    raise ValueError("Disk connection must be provided for Disk strategy")
                return DiskScriptStrategy(disk)
            case "jamf":
                api = kwargs.get('api')
                if not api:
                    raise ValueError("API connection must be provided for Jamf strategy")
                return JamfScriptStrategy(api)
            case _:
                raise ValueError(f"Unknown location type: {location_type}")


    @staticmethod
    def ScriptListStrategy(location_type: str, **kwargs) -> ScriptListStrategy:
        """
        Create a ScriptList strategy object for a given "location_type"

        Args:
            location_type (str): String representation of the location type.  Currently "disk" or "jamf"
        
        Returns:
            ScriptListStrategy: Concrete implementation of ScriptListStrategy
        """
        match location_type:
            case "disk":
                disk = kwargs.get('disk')
                if not disk:
                    raise ValueError("Disk connection must be provided for Disk strategy")
                return DiskScriptListStrategy(disk)
            case "jamf":
                api = kwargs.get('api')
                if not api:
                    raise ValueError("API connection must be provided for Jamf strategy")
                return JamfScriptListStrategy(api)
            case _:
                raise ValueError(f"Unknown location type: {location_type}")


    @staticmethod
    def EaStrategy(location_type: str, **kwargs) -> EaStrategy:
        """
        Create a Ea strategy object for a given "location_type"

        Args:
            location_type (str): String representation of the location type.  Currently "disk" or "jamf"
        
        Returns:
            EaStrategy: Concrete implementation of EaStrategy
        """
        match location_type:
            case "disk":
                disk = kwargs.get('disk')
                if not disk:
                    raise ValueError("Disk connection must be provided for Disk strategy")
                return DiskEaStrategy(disk)
            case "jamf":
                api = kwargs.get('api')
                if not api:
                    raise ValueError("API connection must be provided for Jamf strategy")
                return JamfEaStrategy(api)
            case _:
                raise ValueError(f"Unknown location type: {location_type}")


    @staticmethod
    def EaListStrategy(location_type: str, **kwargs) -> EaListStrategy:
        """
        Create an EaList strategy object for a given "location_type"

        Args:
            location_type (str): String representation of the location type.  Currently "disk" or "jamf"
            EaType (str): String representation of the type of EA we are dealing with.  Currently "computer", "mobile", or "user"
        
        Returns:
            EaListStrategy: Concrete implementation of EaListStrategy
        """
        EaType = kwargs.get('EaType')
        if not EaType:
            raise ValueError("EA type must be provided for any EA strategy")

        match location_type:
            case "disk":
                disk = kwargs.get('disk')
                if not disk:
                    raise ValueError("Disk connection must be provided for Disk strategy")
                return DiskEaListStrategy(disk, EaType)
            case "jamf":
                api = kwargs.get('api')
                if not api:
                    raise ValueError("API connection must be provided for Jamf strategy")
                return JamfEaListStrategy(api, EaType)
            case _:
                raise ValueError(f"Unknown location type: {location_type}")

