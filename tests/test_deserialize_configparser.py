import pytest
import os

from pyser import (ConfigSectionBase, ConfigBase, CompositeConfigOption,
                   SerializeConfigOption, DeserializeConfigOption)

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.ini'
# fruit_basket_missing_field_file = test_data_path + 'fruitBasketMissingField.json'


class BasketDetails(ConfigSectionBase):
    def __init__(self):
        super().__init__('BasketDetails')

        self.name = DeserializeConfigOption()
        self.id = DeserializeConfigOption(name='ref')
        self.intString = DeserializeConfigOption(kind=int)
        self.init_deserialize_config()


class FruitBasket(ConfigBase):
    def __init__(self):
        super().__init__()

        self.name = DeserializeConfigOption(section='BasketDetails')

        self.fruit = DeserializeConfigOption(section='Items')
        self.id = DeserializeConfigOption(name='ref', section='BasketDetails')
        self.intString = DeserializeConfigOption(section='BasketDetails',
                                                 kind=int)
        self.optionalString = DeserializeConfigOption(optional=True)
        self.init_deserialize_config()

        '''
        self.name = SerializeField()
        self.fruit = SerializeField()
        self.iD = SerializeField(name='ref', kind=int)
        self.private = ''  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeField(kind=int)
        self.init_serialize_config()
        '''

        self.private = ''


def test_deserialize_config():
    basket = FruitBasket()
    basket.from_config(fruit_basket_test_file)

    assert basket.name == 'basket'
    assert basket.fruit == 'banana'
    assert basket.id == '1'
    assert basket.intString == 12345


def test_config_section_base():
    details = BasketDetails()
    details.from_config(fruit_basket_test_file)

    assert details.name == 'basket'
    assert details.id == '1'
    assert details.intString == 12345
