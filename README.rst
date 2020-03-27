Pyser
======
.. image:: https://badge.fury.io/py/pyser.svg
    :target: https://badge.fury.io/py/pyser
    :alt: PySer page on the Python Package Index
.. image:: https://github.com/jonnekaunisto/pyser/workflows/Python%20package/badge.svg
  :target: https://github.com/jonnekaunisto/pyser/actions
.. image:: https://codecov.io/gh/jonnekaunisto/pyser/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jonnekaunisto/pyser

PySer is a tool that maps fields from a file to variables in a python object and vice versa.
PySer is a tool that helps with serializing and deserializing data in Python through intuitive mappings in a Python class.


Example PySer Class implementation:

.. code:: python

   from pyser import PySer, Field
   class FruitBasket(JSONBase):
        def __init__(self):
            super().__init__()
            self.name = DeserializeField()
            self.fruit = DeserializeField()
            self.iD = DeserializeField(name='ref', kind=int)
            self.intString = DeserializeField(kind=int)
            self.optionalString = DeserializeField(kind=str, optional=True)
            self.items = DeserializeField(repeated=True)
            self.init_deserialize_json()

            self.name = SerializeField()
            self.fruit = SerializeField()
            self.iD = SerializeField(name="ref", kind=int)
            self.intString = SerializeField(kind=int)
            self.optionalString = SerializeField(optional=True)
            self.items = SerializeField(repeated=True)
            self.register = SerializeField(parent_keys=["checkout"], kind=int)
            self.amount = SerializeField(parent_keys=["checkout"], kind=int)
            
            self.name = "basket"
            self.optionalString = None

            self.fruit = 'banana'
            self.iD = "123"
            self.intString = "12345"
            self.items = ["paper", "rock"]
            self.register = "1"
            self.amount = "10"


Example of serializing to a json file

.. code:: python

    basket = FruitBasket()
    basket.to_json(filename="basket.json")

File contents of basket.json:

.. code:: json

    {
        "name": "basket",
        "fruit": "banana",
        "ref": 123,
        "intString": 12345,
        "items": [
            "paper",
            "rock"
        ],
        "checkout": {
            "register": 1,
            "amount": 10
        }
    }

Similarly deserialization from a json file:

.. code:: Python

    basket = FruitBasket()
    basket.from_json(raw_json=raw_json)


