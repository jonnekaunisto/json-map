import pytest
import os
import sys

currPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currPath + '/../src')
from pyser import DeSerializeField, PySer

class FruitBasket(PySer):
    def __init__(self):
        self.name = DeSerializeField()
        self.fruit = DeSerializeField()
        self.iD = DeSerializeField(name="ref", kind=int)
        self.private = "" # alternatively self.private = DeSerializeField(private=True)
        #self.created = DeSerializeField(kind=Time)
        self.intString = DeSerializeField(kind=int)
        super().__init__()


def test_deserialize():
    basket = FruitBasket()