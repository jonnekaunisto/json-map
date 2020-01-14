import pytest
import os
import sys

from pyser import JSONBase, SerializeField, DeserializeField

basket_json = "{\"name\": \"basket\", \"fruit\": \"banana\", \"ref\": 123, \"intString\": 12345}"


class FruitBasket(JSONBase):
    def __init__(self):
        super().__init__()
        self.name = SerializeField()
        self.fruit = SerializeField()
        self.iD = SerializeField(name="ref", kind=int)
        self.private = ""  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeField(kind=int)
        self.optionalString = SerializeField(optional=True)
        self.init_serialize_json()

        self.name = DeserializeField()
        self.fruit = DeserializeField()
        self.iD = DeserializeField(name="ref", kind=int)
        self.private = ""
        # self.created = DeserializeField(kind=Time)
        self.intString = DeserializeField(kind=int)
        self.init_deserialize_json()

        self.name = "basket"
        self.optionalString = None


class FruitBasketNotCallable(JSONBase):
    def __init__(self):
        super().__init__()
        self.name = SerializeField(kind="not a valid kind")
        self.init_serialize_json()


def test_serialize():
    basket = FruitBasket()
    assert basket.name == 'basket'
    basket.fruit = 'banana'
    basket.iD = "123"
    basket.intString = "12345"

    assert basket.to_json() == basket_json


def test_serialize_file():
    temp_file = 'test_file.json'

    basket = FruitBasket()
    assert basket.name == 'basket'
    basket.fruit = 'banana'
    basket.iD = "123"
    basket.intString = "12345"

    basket.to_json(filename=temp_file)

    with open(temp_file, 'r') as f:
        raw_json = f.read()
    assert raw_json == basket_json
    os.remove(temp_file)


def test_serialize_negative():
    with pytest.raises(Exception, match="Kind needs to be callable"):
        basket = FruitBasketNotCallable()


def test_serialize_str():
    str(SerializeField())
