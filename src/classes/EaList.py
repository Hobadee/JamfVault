from __future__ import annotations
import copy
from src.classes.ObjectList import ObjectList
from src.classes.Ea import Ea


class EaList(ObjectList[Ea]):
    """
    Class to contain and handle multiple Extension Attributes
    """


    # Arithmetic Operators
    def __iand__(self, other):
        """
        This implements the '&=' operator for this class

        This should function by taking list A and B, and combining them into list C, where list C contains ONLY the
        duplicates between lists A and B
        """
        raise NotImplementedError('ExtensionAttributeList.__iand__() not implemented yet!')


    def __ior__(self, other: {Script, ScriptList}) -> self:
        raise NotImplementedError("Copied from ScriptList.py - Check and implement as ExtensionAttributeList")
        """
        This implements the '|=' operator for this class

        This should function by taking list A and B, and combining them into list C, where duplicates are merged down,
        such that list C has all of items A and B, but no duplicates.

        Merging of values between A and B are done using the same method that the Scripts IOR method uses, namely
        individual values from A will override values from B.

        Args:
            other (Script|ScriptList): Other ScriptList to merge into this one

        Returns:
            ScriptList: This ScriptList
        """
        # Copy OTHER to new TEMP ScriptList
        # Loop through all items in SELF
        # For each item in SELF, if match in TEMP is found, OR it and REMOVE from TEMP
        # Once we are done looping, add all items in TEMP to SELF
        temp = copy.deepcopy(other)

        for item in self._scripts:
            try:
                ts = temp.GetByName(item.name)
                item |= ts
                temp.remove(ts)
            except KeyError:
                # GetByName() will throw a KeyError if we can't find the item
                # If this is the case, ignore and go to the next
                pass
        for item in temp:
            self.add(item)
        
        return self

    def __iadd__(self, other):
        raise NotImplementedError("Copied from ScriptList.py - Check and implement as ExtensionAttributeList")
        """
        Handle:
        self._loadStatus
        self._loadStrategy
        self._saveStrategy

        If old == new, keep.  Else wipe
        """
        if isinstance(other, Script):
            self.add(other)
            return self
        elif isinstance(other, ScriptList):
            for s in other:
                self.add(s)
            return self
        raise TypeError(f'Can only add type "Script" or "ScriptList" to a ScriptList!')

    def __isub__(self, other):
        raise NotImplementedError("Copied from ScriptList.py - Check and implement as ExtensionAttributeList")
        pass
