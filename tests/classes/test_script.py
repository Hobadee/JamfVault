from __future__ import annotations

from src.classes.Script import Script
from tests.testDataGenerator import testDataGenerator
import pytest


class TestScriptClasses:

    def test_script_init(self):

        s = Script()

        assert isinstance(s, Script)

        # Test all getters and setters
        # Test __str__ function
        # Test __repr__ function
    
    def test_script_from_json(self):
        pass

    def test_script_str(self):
        pass

    def test_script_repr(self):
        pass

    def test_script_ior(self):

        s1 = Script()
        s2 = Script()

        s1.parameter4 = "S1 P4"
        s2.parameter5 = "S2 P5"
        s1.parameter6 = "S1 P6"
        s2.parameter6 = "S2 P6"

        s1 |= s2

        assert isinstance(s1, Script)
        assert s1.parameter4 == "S1 P4"
        assert s1.parameter5 == "S2 P5"
        assert s1.parameter6 == "S1 P6"


    @pytest.fixture
    @staticmethod
    def GetSetInstance():
        s = Script()
        return s

    @pytest.mark.parametrize("variable_name, variable_type", [
        ("_scriptId","int"),
        ("_name","str"),
        ("_info","str"),
        ("_notes","str"),
        ("_priority","str"),
        ("_parameter4","str"),
        ("_parameter5","str"),
        ("_parameter6","str"),
        ("_parameter7","str"),
        ("_parameter8","str"),
        ("_parameter9","str"),
        ("_parameter10","str"),
        ("_parameter11","str"),
        ("_osRequirements","str"),
        ("_scriptContents","str"),
        ("_categoryId","int"),
        ("_categoryName","str"),
        ("_loadStatus","str"),
        ("_loadStrategy","ScriptStrategy"),
        ("_saveStrategy","ScriptStrategy"),
    ])
    def test_set_get_variable(GetSetInstance, variable_name, variable_type):
        s = Script()

        name = f"{variable_name[1:]}"   # Removing leading underscore
        
        # Dynamically set the variable using a setter method if available, or directly
        setter_method = f"set_{name}"  # Prepending "set_"
        getter_method = f"get_{name}"  # Prepending "get_"
        setter = getattr(s, setter_method)
        getter = getattr(s, getter_method)

        # Set random test data
        data = testDataGenerator.data(variable_type)
        bad_data = testDataGenerator.bad_data(variable_type)

        setter(data)
        if variable_type:
            with pytest.raises(TypeError):
                setter(bad_data)
        assert getter() == data

        # Set new random test data
        data = testDataGenerator.data(variable_type)
        bad_data = testDataGenerator.bad_data(variable_type)

        setattr(s, name, data)
        if variable_type:
            with pytest.raises(TypeError):
                setattr(s, name, bad_data)
        assert getattr(s, name) == data

