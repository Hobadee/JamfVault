from __future__ import annotations

class EaPopups:
    """
    I'm not entirely sure I want this as it's own class right now.

    ...I do, I just don't want to deal with implementation right now.
    """
    
    def __init__(self):
        self._choices = []

    def addChoice(self, choice):
        seaf._choices.push(choice)
