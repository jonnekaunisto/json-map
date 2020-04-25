import pytest
import os

from pyser import (
    ConfigSectionBase,
    ConfigBase,
    SerConfigOption,
    DeserConfigOption,
    SerConfigSection,
    DeserConfigSection,
)
from pyser.configparser import CompositeConfigOption

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + "test_data" + os.sep
fruit_basket_test_file = test_data_path + "fruitBasket.ini"
fruit_basket_missing_field = test_data_path + "fruitBasketMissingField.ini"
fruit_basket_missing_section = test_data_path + "fruitBasketMissingSection.ini"


class BasketDetails(ConfigSectionBase):
    def __init__(self):
        self.name = SerConfigOption()
        self.randomOptional = SerConfigOption(optional=True)

        self.name = DeserConfigOption()
        self.iD = DeserConfigOption(name="ref")
        self.intString = DeserConfigOption(kind=int)


class FruitBasket(ConfigBase):
    def __init__(self):
        self.fruit = SerConfigOption(section="Items")
        self.iD = SerConfigOption(name="ref", section="BasketDetails")
        self.private = ""  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerConfigOption(section="BasketDetails")
        self.optionalString = SerConfigOption(optional=True)

        self.details = SerConfigSection(
            kind=BasketDetails, section="BasketDetails"
        )

        self.name = DeserConfigOption(section="BasketDetails")

        self.fruit = DeserConfigOption(section="Items")
        self.iD = DeserConfigOption(name="ref", section="BasketDetails")
        self.intString = DeserConfigOption(section="BasketDetails", kind=int)

        self.details = DeserConfigSection(
            kind=BasketDetails, section="BasketDetails"
        )
        self.additionalDetails = DeserConfigSection(
            kind=BasketDetails, section="BasketDetails"
        )

        self.private = ""
        self.optionalString = None


def test_deserialize_config():
    basket = FruitBasket()
    details = basket.details
    basket.from_config(fruit_basket_test_file)

    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.iD == "1"
    assert basket.intString == 12345

    assert details.name == "basket"
    assert details.iD == "1"
    assert details.intString == 12345


def test_deserialize_config_negative():
    basket = FruitBasket()

    with pytest.raises(Exception, match='"intString" option not in config'):
        basket.from_config(fruit_basket_missing_field)

    with pytest.raises(Exception, match='"Items" section not in config'):
        basket.from_config(fruit_basket_missing_section)
