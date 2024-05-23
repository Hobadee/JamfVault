from __future__ import annotations

import string
import random
from src.classes.strategies.ScriptStrategies import DummyScriptStrategy
from src.classes.strategies.ScriptListStrategies import DummyScriptListStrategy


class testDataGenerator:


    @staticmethod
    def data(data_type):
        match data_type:
            case "int":
                return testDataGenerator.generate_int_data()
            case "float":
                return testDataGenerator.generate_float_data()
            case "str":
                return testDataGenerator.generate_str_data()
            case "ScriptStrategy":
                return testDataGenerator.generate_ScriptStrategy_data()
            case "ScriptListStrategy":
                return testDataGenerator.generate_ScriptListStrategy_data()
            case None:
                return None
            case _:
                raise ValueError(f"Unsupported data type: {data_type}")


    @staticmethod
    def bad_data(data_type):

        # Support "None" type
        if not data_type:
            data_type = "int"
        
        supported_types = ["int", "float", "str", "ScriptStrategy", "ScriptListStrategy"]
        supported_types.remove(data_type)  # Remove the requested data type from the list

        if supported_types:
            bad_data_type = random.choice(supported_types)
            return testDataGenerator.data(bad_data_type)
        else:
            raise ValueError(f"No other data types supported for generating bad data")
    

    @staticmethod
    def generate_int_data(max=100) -> int:
        return random.randrange(max)

    @staticmethod
    def generate_float_data() -> float:
        return random.random()

    @staticmethod
    def generate_str_data(size=12, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def generate_ScriptStrategy_data():
        return DummyScriptStrategy()

    @staticmethod
    def generate_ScriptListStrategy_data():
        return DummyScriptListStrategy()
