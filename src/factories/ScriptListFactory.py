from __future__ import annotations

from src.classes.ScriptList import ScriptList
#from src.factories.ScriptFactory import ScriptFactory
#from pathlib import Path
import os
#import json


class ScriptListFactory:

    
    #""" Take a directory, walk the directory for scripts, return a ScriptList object with all scripts
    #"""
    #@staticmethod
    #def DirScript(path):
    #    s = ScriptList()
    #    for (dirpath, dirnames, filenames) in os.walk(path):
    #        for f in filenames:
    #            if f.endswith(".sh") or f.endswith(".py"):
    #                s.add(FileScript(os.path.join(dirpath, f)))
    #    return s


    """ Returns an empty ScriptList
    """
    @staticmethod
    def EmptyScriptList():
        s = ScriptList()
        return s

