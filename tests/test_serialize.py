import pytest
import os
import sys

currPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currPath + '/../src')
from pyser import SerializeField, PySer

class FruitBasket(PySer):
    def __init__(self):
        self.name = SerializeField()
        self.fruit = SerializeField()
        self.iD = SerializeField(name="ref", kind=int)
        self.private = "" # alternatively self.private = Field(private=True)
        #self.created = Field(kind=Time)
        self.intString = SerializeField(kind=int)

        super().__init__()
        self.init_serialize()

        self.name = "basket"

def test_serialize():
    basket = FruitBasket()
    assert basket.name == 'basket'
    basket.fruit = 'banana'
    basket.iD = "123"
    basket.intString = "12345"

    assert basket.to_json() == "{\"name\": \"basket\", \"fruit\": \"banana\", \"ref\": 123, \"intString\": 12345}"
