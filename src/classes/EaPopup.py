from __future__ import annotations

class EaPopup:
    
    def __init__(self):
        self._choices = []

        # Index for iterator
        self._index = 0


    def addChoice(self, choice):
        self._choices.append(choice)


    def add(self, popup):
        self._choices.append(popup)


    def remove(self, popup):
        self._choices.remove(popup)


    def len(self):
        return self.__len__()


    def __len__(self):
        """
        Add support for the len() command
        """
        return len(self._choices)


    # Make indexable
    def __getitem__(self, index):
        return self._choices[index]

    def __setitem__(self, index, newvalue):
        self._choices[index] = newvalue



    def __contains__(self, item):
        for current_item in self._choices:
            if item == current_item:
                return True
        return False



    # Make iterable
    def __iter__(self):
        return iter(self._choices)

    
    def __next__(self):
        if self._index < len(self._choices):
            s = self._choices[self._index]
            self._index += 1
            return s
        else:
            raise StopIteration
    
