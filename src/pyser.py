from collections import defaultdict
import json


class PySer():
    def __init__(self):
       self.__field_dict = {}

    def init_serialize(self):        
        for field_name, field in self.__dict__.items():
            if type(field) is SerializeField:
                if field_name in self.__field_dict:
                      self.__field_dict[field_name].serialize = field
                else:
                     self.__field_dict[field_name] = Field(serialize=field)


    def init_deserialize(self):        
        for field_name, field in self.__dict__.items():
            if type(field) is DeSerializeField:
                if field_name in self.__field_dict:
                    self.__field_dict[field_name].deserialize = field
                else:
                    self.__field_dict[field_name] = Field(deserialize==field)

            


    def to_json(self, filename=None):
        json_dict = {}
        for field_name, field in self.__field_dict.items():
            print(field_name)
            kind = field.serialize.kind
            json_value = None
            if kind is None:
                json_value = self.__dict__[field_name]
            else:
                json_value = kind(self.__dict__[field_name])

            if field.serialize.name is not None:
                json_dict[field.serialize.name] = json_value
            else:
                json_dict[field_name] = json_value

        if filename is None:
            return json.dumps(json_dict)


class Field():
    def __init__(self, serialize=None, deserialize=None):
        self.serialize = serialize
        self.deserialize = deserialize


class DeSerializeField():
    '''Field
    name:
        name of the field that should be deserialized to, default is the name of the variable
    kind:
        the type of the variable should be deserialized to, default is what the serialized variable is
    '''
    def __init__(self, name=None, kind=None):
        self.name = name
        self.kind = kind

    def __str__(self):
        return "(name: {0}, kind: {1}, serialized_field: {2})".format(self.name, 
                    self.kind, self.serialize_field)

    __repr__ = __str__


class SerializeField():
    def __init__(self, name=None, kind=None):
        self.name = name
        self.kind = kind
