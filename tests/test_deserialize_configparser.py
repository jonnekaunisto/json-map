import pytest
import os

from pyser import (ConfigSectionBase, ConfigBase,
                   SerializeConfigOption, DeserializeConfigOption,
                   SerializeConfigSection, DeserializeConfigSection)
from pyser.configparser_resources import CompositeConfigOption

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.ini'
fruit_basket_missing_field = test_data_path + 'fruitBasketMissingField.ini'
fruit_basket_missing_section = test_data_path + 'fruitBasketMissingSection.ini'


class BasketDetails(ConfigSectionBase):
    def __init__(self):
        super().__init__()

        self.name = SerializeConfigOption()
        self.randomOptional = SerializeConfigOption(optional=True)
        self.init_serialize_config()

        self.name = DeserializeConfigOption()
        self.iD = DeserializeConfigOption(name='ref')
        self.intString = DeserializeConfigOption(kind=int)
        self.init_deserialize_config()


class FruitBasket(ConfigBase):
    def __init__(self):
        super().__init__()

        self.fruit = SerializeConfigOption(section='Items')
        self.iD = SerializeConfigOption(name='ref', section='BasketDetails')
        self.private = ''  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeConfigOption(section='BasketDetails')
        self.optionalString = SerializeConfigOption(optional=True)

        self.details = SerializeConfigSection('BasketDetails')

        self.init_serialize_config()

        self.name = DeserializeConfigOption(section='BasketDetails')

        self.fruit = DeserializeConfigOption(section='Items')
        self.iD = DeserializeConfigOption(name='ref', section='BasketDetails')
        self.intString = DeserializeConfigOption(section='BasketDetails',
                                                 kind=int)

        self.details = DeserializeConfigSection(section='BasketDetails')
        self.additionalDetails = DeserializeConfigSection(section='BasketDetails')

        self.init_deserialize_config()

        self.private = ''
        self.optionalString = None
        self.details = BasketDetails()
        self.additionalDetails = BasketDetails()

        self.init_section_values()


def test_deserialize_config():
    basket = FruitBasket()
    details = basket.details
    basket.from_config(fruit_basket_test_file)

    assert basket.name == 'basket'
    assert basket.fruit == 'banana'
    assert basket.iD == '1'
    assert basket.intString == 12345

    assert details.name == 'basket'
    assert details.iD == '1'
    assert details.intString == 12345


def test_deserialize_config_negative():
    basket = FruitBasket()

    with pytest.raises(Exception, match='"intString" option not in config'):
        basket.from_config(fruit_basket_missing_field)

    with pytest.raises(Exception, match='"Items" section not in config'):
        basket.from_config(fruit_basket_missing_section)
