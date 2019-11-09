JSON Map
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
class FruitBasket(jsonMap):
    def __init__(self):
        self.name = jsonMap.Field()
        self.fruit = jsonMap.Field()
        self.iD = jsonMap.Field(name="ref", int)
        self.private = "" # alternatively self.private = jsonMap.Field(private=True)
        self.created = jsonMap.Field(type=Time)
        self.intString = jsonMap.Field(type=int, jsonType=string)
```
