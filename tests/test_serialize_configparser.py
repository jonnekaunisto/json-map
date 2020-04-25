import pytest
import os
import configparser

from pyser import (
    ConfigSectionBase,
    ConfigBase,
    SerConfigOption,
    DeserConfigOption,
    SerConfigSection,
    DeserConfigSection,
)

from pyser.configparser import CompositeConfigOption, CompositeConfigSection

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + "test_data" + os.sep
fruit_basket_test_file = test_data_path + "fruitBasket.ini"


class BasketDetails(ConfigSectionBase):
    def __init__(self):
        self.name = DeserConfigOption()
        self.randomOptional = DeserConfigOption(optional=True)

        self.name = SerConfigOption()
        self.iD = SerConfigOption(name="ref")
        self.intString = SerConfigOption()


class FruitBasket(ConfigBase):
    def __init__(self):
        self.fruit = DeserConfigOption(section="Items")
        self.iD = DeserConfigOption(name="ref", section="BasketDetails")
        self.intString = DeserConfigOption(section="BasketDetails", kind=int)

        self.details = DeserConfigSection(
            kind=BasketDetails, section="BasketDetails"
        )

        self.name = SerConfigOption(section="BasketDetails")
        self.fruit = SerConfigOption(section="Items")
        self.iD = SerConfigOption(name="ref", section="BasketDetails")
        # self.created = Field(kind=Time)
        self.intString = SerConfigOption(section="BasketDetails")
        self.optionalString = SerConfigOption(optional=True)

        self.optionalString = None
        self.details = BasketDetails()


def test_serialize_config():
    basket = FruitBasket()

    basket.name = "basket"
    basket.iD = 1
    basket.intString = 12345
    basket.fruit = "banana"

    config = basket.to_config()

    assert config["BasketDetails"]["name"] == "basket"
    assert config["BasketDetails"]["ref"] == "1"
    assert config["BasketDetails"]["intString"] == "12345"
    assert config["Items"]["fruit"] == "banana"


def test_serialize_config_file():
    temp_file = "temp.ini"
    basket = FruitBasket()
    basket.name = "basket"
    basket.iD = 1
    basket.intString = 12345
    basket.fruit = "banana"

    basket.to_config(filename=temp_file)

    config = configparser.RawConfigParser()
    config.read(temp_file)

    assert config["BasketDetails"]["name"] == "basket"
    assert config["BasketDetails"]["ref"] == "1"
    assert config["BasketDetails"]["intString"] == "12345"
    assert config["Items"]["fruit"] == "banana"

    with open(temp_file, "r") as f:
        raw_json = f.read()
    os.remove(temp_file)


def test_serialize_config_str():
    serialize = SerConfigOption()
    deserialize = DeserConfigOption()

    str(CompositeConfigOption(serialize=serialize, deserialize=deserialize))

    serialize = SerConfigSection(kind=object, section="something")
    deserialize = SerConfigSection(kind=object, section="something")

    str(CompositeConfigSection(serialize=serialize, deserialize=deserialize))
