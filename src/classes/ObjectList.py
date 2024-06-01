from __future__ import annotations
from typing import TypeVar, Generic, List
import abc

T = TypeVar('T')

class ObjectList(Generic[T]):
    """
    Base class to contain and handle a collection of a type of object

    I'm using the terms "object" and "item" a little interchangably here.  Sorry for
    the confusion.

    Attributes:
        _items (List): Array of objects.  Should all be the same type
    """


    def __init__(self):
        """
        Class init function
        """
        self._items: List[T] = []

        # Index for iterator
        self._index = 0


    def add(self, item: Generic[T]) -> self:
        """
        Adds an object to the list

        Args:
            item (Generic[T]): Object item of type T to add

        Returns:
            self: This object
        """
        self._items.append(item)

        return self


    def remove(self, item: Generic[T]) -> self:
        """
        Removes a given object from the list

        You can get the object using a GetBy___ function
        
        Args:
            item (Generic[T]): Object item of type T to remove

        Returns:
            self: This object
        """
        self._items.remove(item)

        return self


    def len(self) -> int:
        """
        Returns the number of items in this list object

        Returns:
            int: Number of items in this list
        """
        # Redirect to special __len__ function
        return self.__len__()


    def GetById(self, itemId: int) -> Generic[T]:
        """
        Searches for an item with a given ID and returns it

        Args:
            itemId (int): ID to search for

        Returns:
            Generic[T]: First item with a matching ID
        """
        for item in self._items:
            if item.itemId == itemId:
                return item
        # "Cannot find id:1 in array of <class 'str'>!"
        raise KeyError(f'Cannot find id:{itemId} in array of {get_args(self.__orig_class__)[0]}!')


    def GetByName(self, name: str) -> Generic[T]:
        """
        Searches for an item with a given name and returns it

        Args:
            name (str): Name to search for

        Returns:
            Generic[T]: First item with a matching name
        """
        for item in self._items:
            if item.name == name:
                return item
        # "Cannot find "Some Object Name" in array of <class 'str'>!"
        raise KeyError(f'Cannot find "{name}" in array of {get_args(self.__orig_class__)[0]}!')


    def ExistsById(self, itemId: int) -> bool:
        """
        Returns whether an item with a given ID exists or not

        Args:
            itemId (int): ID to search for

        Returns:
            bool: True if item with ID exists, False otherwise
        """
        for item in self._items:
            if item.itemId == itemId:
                return True
        return False


    def ExistsByName(self, name: str) -> bool:
        """
        Returns whether an item with a given name exists or not

        Args:
            name (str): Name to search for

        Returns:
            bool: True if item with name exists, False otherwise
        """
        for item in self._items:
            if item.name == name:
                return True
        return False


    def __contains__(self, item: Generic[T]) -> bool:
        """
        __contains__ magic method to handle things like `in`
        
        Args:
            item (T): Object item of type T to remove

        Returns:
            bool: True if item exists, False otherwise
        """
        for current_item in self._items:
            if item == current_item:
                return True
        return False
    

    def __len__(self) -> int:
        """
        __len__ magic method to handle things like `len()`

        Returns:
            int: Number of items contained in this ObjectList
        """
        return len(self._items)
    

    # Make indexable
    def __getitem__(self, index: int) -> Generic[T]:
        """
        __getitem__ magic method to return items at a given index

        Args:
            index (int): Index to return
        
        Returns:
            Generic[T]: Item at given index
        """
        return self._items[index]

    def __setitem__(self, index: int, newvalue: Generic[T]) -> None:
        """
        __setitem__ magic method to set an item at a given index

        Args:
            index (int): Index to set
            newvalue (Generic[T]): New value to set `index` to
        """
        self._items[index] = newvalue


    # Make reversable
    # This doesn't currently work
    #def __reversed__(self):
    #    return type(self)(reversed(self._scripts))


    # Make iterable
    def __iter__(self):
        """
        __iter__ magic method to return the iterable object
        """
        return iter(self._items)

    
    def __next__(self) -> Generic[T]:
        """
        __next__ magic method to return the next iterable object

        Returns:
            Generic[T]: Next object in iteration sequence
        
        Raises:
            StopIteration: When the index overflows the list
        """
        if self._index < len(self):
            i = self._items[self._index]
            self._index += 1
            return i
        else:
            raise StopIteration
    

    # Arithmetic Operators
    @abc.abstractmethod
    def __iand__(self, other):
        """
        This implements the '&=' operator for this class

        This should function by taking list A and B, and combining them into list C, where list C contains ONLY the
        duplicates between lists A and B
        """
        raise NotImplementedError('ExtensionAttributeList.__iand__() not implemented yet!')


    @abc.abstractmethod
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
            Generic[T]: This ObjectList, combined with the other ObjectList.
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


    @abc.abstractmethod
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


    @abc.abstractmethod
    def __isub__(self, other):
        raise NotImplementedError("Copied from ScriptList.py - Check and implement as ExtensionAttributeList")
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

