from __future__ import annotations
import copy


class ScriptList:


    """ Class init function
    """
    def __init__(self):
        self._scripts = []

        # Index for iterator
        self._index = 0


    """ Adds a script object to the ScriptList
    """
    def add(self, script):
        self._scripts.append(script)


    """ Removes a given script object from the ScriptList

        You can get the script object using a GetBy___ function
    """
    def remove(self, script):
        # Will this work??
        self._scripts.remove(script)


    """ Returns the number of scripts in this ScriptList object
    """
    def len(self):
        # Redirect to special __len__ function
        return self.__len__()


    """ Searches for a script with a given ID and returns it
    """
    def GetById(self, scriptId):
        for item in self._scripts:
            if item.scriptId == scriptId:
                return item
        raise KeyError(f'Cannot find {scriptId} in scripts!')


    """ Searches for a script with a given name and returns it
    """
    def GetByName(self, name):
        for item in self._scripts:
            if item.name == name:
                return item
        raise KeyError(f'Cannot find {name} in scripts!')


    """ Searches for a script with a given ID and returns it
    """
    def ExistsById(self, scriptId):
        for item in self._scripts:
            if item.scriptId == scriptId:
                return True
        return False


    """ Searches for a script with a given name and returns it
    """
    def ExistsByName(self, name):
        for item in self._scripts:
            if item.name == name:
                return True
        return False


    # This probably needs some cleanup.  Placeholder for now.
    def __contains__(self, item):
        for current_item in self._scripts:
            if item == current_item:
                return True
        return False
    

    # Support len()
    def __len__(self):
        return len(self._scripts)
    

    # Make indexable
    def __getitem__(self, index):
        return self._scripts[index]

    def __setitem__(self, index, newvalue):
        self._scripts[index] = newvalue


    # Make reversable
    # This doesn't currently work
    #def __reversed__(self):
    #    return type(self)(reversed(self._scripts))


    # Make iterable
    def __iter__(self):
        return iter(self._scripts)

    
    def __next__(self):
        if self._index < len(self._scripts):
            s = self._scripts[self._index]
            self._index += 1
            return s
        else:
            raise StopIteration
    

    # Arithmetic Operators
    """ This implements the '&=' operator for this class

        This should function by taking list A and B, and combining them into list C, where list C contains ONLY the
        duplicates between lists A and B
    """
    def __iand__(self, other):
        raise NotImplementedError('ScriptList.remove not implemented yet!')


    def __ior__(self, other: {Script, ScriptList}) -> self:
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
        pass


    # We should probably implement the following special methods to allow easier operations:
    # https://realpython.com/python-magic-methods/
    # +=	.__iadd__(self, other)
    # -=	.__isub__(self, other)
    # &	    .__and__(self, other)  (Returns new item)
    """
        This should work for and/or/xor functions:
            temp = copy.deepcopy(self)
            temp &|^= other
            return temp
    """
    # |	    .__or__(self, other)
    # ^	    .__xor__(self, other)
    # ~     .__invert__()
    # &=	.__iand__(self, other)  (Returns same item)
    # |=	.__ior__(self, other)
    # ^=	.__ixor__(self, other)

    # ==	.__eq__(self, other)
    # !=	.__ne__(self, other)
    """
        >>> s1 = {"a", "b", "c"}
        >>> s2 = {"d", "e", "f"}

        >>> # OR, | 
        >>> s1 | s2
        {'a', 'b', 'c', 'd', 'e', 'f'}
        >>> s1                                                     # `s1` is unchanged
        {'a', 'b', 'c'}

        >>> # In-place OR, |=
        >>> s1 |= s2
        >>> s1                                                     # `s1` is reassigned
        {'a', 'b', 'c', 'd', 'e', 'f'}
    """

