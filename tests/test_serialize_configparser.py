import pytest
import os
import configparser

from pyser import (ConfigSectionBase, ConfigBase,
                   SerializeConfigOption, DeserializeConfigOption,
                   SerializeConfigSection, DeserializeConfigSection)

from pyser.configparser_resources import (CompositeConfigOption, 
                                          CompositeConfigSection)

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.ini'


class BasketDetails(ConfigSectionBase):
    def __init__(self):
        super().__init__()

        self.name = DeserializeConfigOption()
        self.randomOptional = DeserializeConfigOption(optional=True)
        self.init_deserialize_config()

        self.name = SerializeConfigOption()
        self.iD = SerializeConfigOption(name='ref')
        self.intString = SerializeConfigOption()
        self.init_serialize_config()


class FruitBasket(ConfigBase):
    def __init__(self):
        super().__init__()

        self.fruit = DeserializeConfigOption(section='Items')
        self.iD = DeserializeConfigOption(name='ref', section='BasketDetails')
        self.intString = DeserializeConfigOption(section='BasketDetails',
                                                 kind=int)

        self.details = DeserializeConfigSection(section='BasketDetails')
        self.init_deserialize_config()

        self.name = SerializeConfigOption(section='BasketDetails')
        self.fruit = SerializeConfigOption(section='Items')
        self.iD = SerializeConfigOption(name='ref', section='BasketDetails')
        self.private = ''  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeConfigOption(section='BasketDetails')
        self.optionalString = SerializeConfigOption(optional=True)

        self.init_serialize_config()

        self.private = ''
        self.optionalString = None
        self.details = BasketDetails()

        self.init_section_values()


def test_serialize_config():
    basket = FruitBasket()

    basket.name = 'basket'
    basket.iD = 1
    basket.intString = 12345
    basket.fruit = 'banana'

    config = basket.to_config()

    assert config['BasketDetails']['name'] == 'basket'
    assert config['BasketDetails']['ref'] == '1'
    assert config['BasketDetails']['intString'] == '12345'
    assert config['Items']['fruit'] == 'banana'


def test_serialize_config_file():
    temp_file = "temp.ini"
    basket = FruitBasket()
    basket.name = 'basket'
    basket.iD = 1
    basket.intString = 12345
    basket.fruit = 'banana'

    basket.to_config(filename=temp_file)

    config = configparser.RawConfigParser()
    config.read(temp_file)

    assert config['BasketDetails']['name'] == 'basket'
    assert config['BasketDetails']['ref'] == '1'
    assert config['BasketDetails']['intString'] == '12345'
    assert config['Items']['fruit'] == 'banana'

    with open(temp_file, 'r') as f:
        raw_json = f.read()
    os.remove(temp_file)


def test_serialize_config_str():
    serialize = SerializeConfigOption()
    deserialize = DeserializeConfigOption()

    str(CompositeConfigOption(serialize=serialize, deserialize=deserialize)) 

    serialize = SerializeConfigSection(section="something")
    deserialize = SerializeConfigSection(section="something")

    str(CompositeConfigSection(serialize=serialize, deserialize=deserialize))   
