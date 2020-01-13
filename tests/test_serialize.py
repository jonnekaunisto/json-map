import pytest
import os
import sys

currPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currPath + '/../src')
from pyser import SerializeField, DeserializeField, PySer


class FruitBasket(PySer):
    def __init__(self):
        super().__init__()
        self.name = SerializeField()
        self.fruit = SerializeField()
        self.iD = SerializeField(name="ref", kind=int)
        self.private = ""  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeField(kind=int)
        self.init_serialize()

        self.name = DeserializeField()
        self.fruit = DeserializeField()
        self.iD = DeserializeField(name="ref", kind=int)
        self.private = ""
        # self.created = DeserializeField(kind=Time)
        self.intString = DeserializeField(kind=int)
        self.init_deserialize()

        self.name = "basket"


def test_serialize():
    basket = FruitBasket()
    assert basket.name == 'basket'
    basket.fruit = 'banana'
    basket.iD = "123"
    basket.intString = "12345"

    assert basket.to_json() == "{\"name\": \"basket\", \"fruit\": \"banana\", \"ref\": 123, \"intString\": 12345}"
