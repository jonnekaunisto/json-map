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

Example:

.. code:: python

   from pyser import PySer, Field
   class FruitBasket(PySer):
       def __init__(self):
            super().__init__()
            self.name = DeserializeField()
            self.fruit = DeserializeField()
            self.iD = DeserializeField(name="ref", kind=int)
            self.private = ""
            # self.created = DeserializeField(kind=Time)
            self.intString = DeserializeField(kind=int)
            self.init_deserialize()


In Python this could be represented by:

.. code:: Python

    basket = FruitBasket()
    basket.from_json(raw_json=raw_json)


