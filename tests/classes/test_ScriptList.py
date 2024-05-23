from __future__ import annotations

from src.classes.Script import Script
from src.classes.ScriptList import ScriptList


class TestScriptClasses:

    def test_ScriptList(self):
        s = ScriptList()

        assert isinstance(s, ScriptList)

        # Test __reversed__
        # Test Iteration
        #   __iter__
        #   __next__
        # Test iand &=
        # 


    #def test_ScriptList_reverse(self):
    #    sl = ScriptList()
    #
    #    s0 = Script()
    #    s1 = Script()
    #    s2 = Script()
    #
    #    s0.name = "Script 0"
    #    s1.name = "Script 1"
    #    s2.name = "Script 2"
    #
    #    sl.add(s0)
    #    sl.add(s1)
    #    sl.add(s2)
    #    assert reversed(sl) == [s2, s1, s0]


    def test_ScriptList_contains(self):
        sl = ScriptList()

        s0 = Script()
        s1 = Script()
        s2 = Script()

        s0.name = "Script 0"
        s1.name = "Script 1"
        s2.name = "Script 2"
        
        sl.add(s0)
        sl.add(s2)
        
        assert s0 in sl
        assert not s1 in sl


    def test_ScriptList_add(self):
        sl = ScriptList()

        s0 = Script()
        s1 = Script()
        s2 = Script()

        s0.name = "Script 0"
        s1.name = "Script 1"
        s2.name = "Script 2"

        assert sl._scripts == []
        
        sl.add(s0)
        assert sl._scripts == [s0]

        sl.add(s1)
        assert sl._scripts == [s0, s1]

        sl.add(s2)
        assert sl._scripts == [s0, s1, s2]


    def test_ScriptList_remove(self):
        sl = ScriptList()

        s0 = Script()
        s1 = Script()
        s2 = Script()

        s0.name = "Script 0"
        s1.name = "Script 1"
        s2.name = "Script 2"
        
        sl.add(s0)
        sl.add(s1)
        sl.add(s2)
        
        sl.remove(s1)
        assert sl._scripts == [s0, s2]

        sl.remove(s0)
        assert sl._scripts == [s2]

        sl.remove(s2)
        assert sl._scripts == []


    def test_ScriptList_len(self):
        sl = ScriptList()

        s0 = Script()
        s1 = Script()
        s2 = Script()

        s0.name = "Script 0"
        s1.name = "Script 1"
        s2.name = "Script 2"

        sl.add(s0)
        sl.add(s1)
        sl.add(s2)

        assert sl.len() == 3
        assert len(sl) == 3


    def test_ScriptList_getitem(self):
        sl = ScriptList()

        s0 = Script()
        s1 = Script()
        s2 = Script()

        s0.name = "Script 0"
        s1.name = "Script 1"
        s2.name = "Script 2"

        sl.add(s0)
        sl.add(s1)
        sl.add(s2)

        assert sl[0] == s0
        assert sl[1] == s1
        assert sl[2] == s2


    def test_ScriptList_ior(self):

        sl1 = ScriptList()
        sl2 = ScriptList()

        s1 = Script()
        s2 = Script()
        s3 = Script()
        s4a = Script()
        s4b = Script()

        s1.name = "Script 1"
        s1.info = "SL1 only"

        s2.name = "Script 2"
        s2.info = "SL2 only"

        s3.name = "Script 3"
        s3.info = "SL1 & SL2"

        s4a.name = "Script 4"
        s4a.info = "SL1 & SL2 w/diffs"
        s4a.parameter4 = "4a P4 - 4a only"
        s4a.parameter6 = "4a P6 - 4a/4b"
        s4b.name = "Script 4"
        s4b.parameter5 = "4b P5 - 4b only"
        s4b.parameter6 = "4b P6 - 4a/4b"

        sl1.add(s1)
        sl2.add(s2)
        sl1.add(s3)
        sl2.add(s3)
        sl1.add(s4a)
        sl2.add(s4b)

        sl1 |= sl2

        assert isinstance(sl1, ScriptList)

        assert isinstance(sl1.GetByName("Script 1"), Script)
        assert isinstance(sl1.GetByName("Script 2"), Script)
        assert isinstance(sl1.GetByName("Script 3"), Script)

        s4 = sl1.GetByName("Script 4")
        assert s4.parameter4 == "4a P4 - 4a only"
        assert s4.parameter5 == "4b P5 - 4b only"
        assert s4.parameter6 == "4a P6 - 4a/4b"
        assert s4.parameter7 == None
