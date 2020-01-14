import pytest
import os

from pyser import (ConfigSectionBase, ConfigBase, CompositeConfigOption,
                   SerializeConfigOption, DeserializeConfigOption)

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.ini'
#fruit_basket_missing_field_file = test_data_path + 'fruitBasketMissingField.json'


class BasketDetails(ConfigSectionBase):
    def __init__(self):
        pass


class FruitBasket(ConfigBase):
    def __init__(self):
        super().__init__()

        self.name = DeserializeConfigOption(section="BasketDetails")
        '''
        self.fruit = DeserializeConfigOption()
        self.iD = DeserializeConfigOption(name='ref')
        self.intString = DeserializeConfigOption(kind=int)
        self.optionalString = DeserializeConfigOption(optional=True)
        '''
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
