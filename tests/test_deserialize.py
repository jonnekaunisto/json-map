import pytest
import os
import sys

currPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currPath + '/../src')
from pyser import DeSerializeField, PySer

raw_json = '{\"name\": \"basket\", \"fruit\": \"banana\", \"ref\": 123, \"intString\": 12345}'


class FruitBasket(PySer):
    def __init__(self):
        self.name = DeSerializeField()
        self.fruit = DeSerializeField()
        self.iD = DeSerializeField(name="ref", kind=int)
        self.private = ""
        # self.created = DeSerializeField(kind=Time)
        self.intString = DeSerializeField(kind=int)
        super().__init__()
        self.init_deserialize()


def test_deserialize():
    basket = FruitBasket()
    print(basket.__dict__)

    basket.from_json(raw_json=raw_json)
    print(basket.__dict__)
    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.ref == 123
    assert basket.intString == 12345
