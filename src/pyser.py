from collections import defaultdict
import json


class PySer():
    def __init__(self):
        self.__field_dict = {}

    def init_serialize(self):
        '''initializes all the variables that have to do with serializing
        '''
        for field_name, field in self.__dict__.items():
            if type(field) is SerializeField:
                # If name is not specified use the name of the variable
                if field.name is None:
                    field.name = field_name

                if field_name in self.__field_dict:
                    self.__field_dict[field_name].serialize = field
                else:
                    self.__field_dict[field_name] = Field(serialize=field)

                self.__dict__[field_name] = None

    def init_deserialize(self):
        '''initializes all the variables that have to do with deserializing
        '''
        for field_name, field in self.__dict__.items():
            if type(field) is DeserializeField:
                if field.name is None:
                    field.name = field_name

                if field_name in self.__field_dict:
                    self.__field_dict[field_name].deserialize = field
                else:
                    self.__field_dict[field_name] = Field(deserialize=field)
                self.__dict__[field_name] = None

    def to_json(self, filename=None):
        json_dict = {}
        for field_name, field in self.__field_dict.items():
            kind = field.serialize.kind
            json_value = None
     
            json_value = kind(self.__dict__[field_name])

            json_dict[field.serialize.name] = json_value

        if filename is None:
            return json.dumps(json_dict)

        with open(filename, 'w') as f:
            f.write(json.dumps(json_dict))

    def from_json(self, filename=None, raw_json=None):
        if filename is not None:
            with open(filename, 'r') as f:
                raw_json = f.read()
        elif raw_json is None:
            raise Exception('Specify filename or raw json')

        data_dict = json.loads(raw_json)

        for field_name, field in self.__field_dict.items():
            deserialize = field.deserialize
            if deserialize.name not in data_dict:
                raise Exception('{} field not found in the json'.format(
                    deserialize.name))

            self.__dict__[deserialize.name] = field.deserialize.kind(
                data_dict[deserialize.name])


class Field():
    def __init__(self, serialize=None, deserialize=None):
        self.serialize = serialize
        self.deserialize = deserialize


class DeserializeField():
    '''Field
    name:
        name of the field that should be deserialized from, default is the
        name of the variable
    kind:
        the type of the variable should be deserialized to, default is what
        the deserialized      variable is
    '''
    def __init__(self, name=None, kind=lambda x: x):
        self.name = name
        self.kind = kind

        if not callable(kind):
            raise Exception("Kind needs to be callable")

    def __str__(self):
        return "(name: {0}, kind: {1})".format(
             self.name, self.kind)

    __repr__ = __str__


class SerializeField():
    '''SerializeField
    name:
        name of the field that should serialize to, defaults to the variable
        name
    kind:
        the type that the field should be serialized to, defaults to the type
        that the variable is
    '''
    def __init__(self, name=None, kind=lambda x: x):
        self.name = name
        self.kind = kind

        if not callable(kind):
            raise Exception("Kind needs to be callable")

    def __str__(self):
        return "(name: {0}, kind: {1})".format(
            self.name, self.kind)

    __repr__ = __str__
