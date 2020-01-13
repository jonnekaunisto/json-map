import pytest
import os
import sys

currPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currPath + '/../src')
from pyser import SerializeField, DeserializeField, PySer

raw_json = '{\"name\": \"basket\", \"fruit\": \"banana\", \"ref\": 123, \"intString\": 12345}'
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.json'
fruit_basket_missing_field_file = test_data_path + 'fruitBasketMissingField.json'


class FruitBasket(PySer):
    def __init__(self):
        super().__init__()
        self.name = DeserializeField()
        self.fruit = DeserializeField()
        self.iD = DeserializeField(name='ref', kind=int)
        self.private = ''
        # self.created = DeserializeField(kind=Time)
        self.intString = DeserializeField(kind=int)
        self.init_deserialize()

        self.name = SerializeField()
        self.fruit = SerializeField()
        self.iD = SerializeField(name='ref', kind=int)
        self.private = ''  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeField(kind=int)
        self.init_serialize()


class FruitBasketNotCallable(PySer):
    def __init__(self):
        super().__init__()
        self.name = DeserializeField(kind="not a valid kind")
        self.init_deserialize()


def test_deserialize_raw_json():
    basket = FruitBasket()
    basket.from_json(raw_json=raw_json)
    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.ref == 123
    assert basket.intString == 12345


def test_deserialize_file():
    basket = FruitBasket()
    basket.from_json(filename=fruit_basket_test_file)
    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.ref == 123
    assert basket.intString == 12345


def test_deserialize_negative():
    with pytest.raises(Exception, match="Kind needs to be callable"):
        basket = FruitBasketNotCallable()

    with pytest.raises(Exception, match='Specify filename or raw json'):
        basket = FruitBasket()
        basket.from_json()

    with pytest.raises(Exception, match='fruit field not found in the json'):
        basket = FruitBasket()
        basket.from_json(filename=fruit_basket_missing_field_file)


def test_deserialize_str():
    str(DeserializeField())
