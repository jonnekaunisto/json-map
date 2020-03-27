Pyser
======
.. image:: https://badge.fury.io/py/pyser.svg
    :target: https://badge.fury.io/py/pyser
    :alt: PySer page on the Python Package Index
.. image:: https://github.com/jonnekaunisto/pyser/workflows/Python%20package/badge.svg
  :target: https://github.com/jonnekaunisto/pyser/actions
.. image:: https://codecov.io/gh/jonnekaunisto/pyser/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jonnekaunisto/pyser

PySer is a tool that helps with serializing and deserializing data in Python through intuitive mappings in a Python class.

Examples
--------

JSON serializing and deserializing class

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


Serializing to a JSON file

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

Installation
------------

**Installation by hand:** you can download the source files from PyPi or Github:

.. code:: bash

    $ (sudo) python setup.py install

**Installation with pip:** make sure that you have ``pip`` installed, type this in a terminal:

.. code:: bash

    $ (sudo) pip install pyser

Documentation
-------------

Running `build_docs` has additional dependencies that require installation.

.. code:: bash

    $ (sudo) pip install pyser[docs]

Running Tests
-------------
Run the python command

.. code:: bash 

   python setup.py test

Contribute
----------
1. Fork the repository from Github
2. Clone your fork 

.. code:: bash 

   git clone https://github.com/yourname/pyser.git

3. Add the main repository as a remote

.. code:: bash

    git remote add upstream https://github.com/jonnekaunisto/pyser.git

4. Create a pull request and follow the guidelines


Maintainers
-----------
jonnekaunisto (owner)
