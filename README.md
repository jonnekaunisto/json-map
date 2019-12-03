Pyser
=======

Plan
----

JSON map will be a module that will allow mapping keys in JSON to a value in a python object and vice versa. This will help with serializing and deserializing complex Python objects.

The implementation will look somewhat similar to Golang's implementation, which uses built in tags for fields to define what key the struct value maps to.

Example:
```Golang
type FruitBasket struct {
    Name    string
    Fruit   []string
    Id      int64  `json:"ref"`
    private string // An unexported field is not encoded.
    Created time.Time
    IntString int64 `json:",string"`
}
```


In Python this could be represented by:

```Python
from pyser import SerializeField, PySer

class FruitBasket(PySer):
    def __init__(self):
        self.name = SerializeField()
        self.fruit = SerializeField(kind=list)
        self.iD = SerializeField(name="ref", kind=int)
        #self.created = Field(kind=Time)
        self.intString = SerializeField(kind=string)

        super().__init__()
        self.init_serialize()

        self.name = "basket" # setting default value after initializing fields
        self.private = "" # alternatively self.private = Field(private=True)

```

```Python
basket = FruitBasket()
basket.to_json('basket.json')
```

The init function from super class will read all the fields from the object and make store them.
