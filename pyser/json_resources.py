from collections import defaultdict
import json


class JSONBase():
    def __init__(self):
        self.__field_dict = {}

    def init_serialize_json(self):
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
                    self.__field_dict[field_name] = CompositeField(
                        serialize=field)

                self.__dict__[field_name] = None

    def init_deserialize_json(self):
        '''initializes all the variables that have to do with deserializing
        '''
        for field_name, field in self.__dict__.items():
            if type(field) is DeserializeField:
                if field.name is None:
                    field.name = field_name

                if field_name in self.__field_dict:
                    self.__field_dict[field_name].deserialize = field
                else:
                    self.__field_dict[field_name] = CompositeField(
                        deserialize=field)
                self.__dict__[field_name] = None

    def to_json(self, filename=None):
        json_dict = {}
        for field_name, field in self.__field_dict.items():
            if self.__dict__[field_name] is None and field.serialize.optional:
                continue

            kind = field.serialize.kind
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

            if deserialize.name in data_dict:
                self.__dict__[deserialize.name] = field.deserialize.kind(
                    data_dict[deserialize.name])
            elif not deserialize.optional:
                raise Exception('{} field not found in the json'.format(
                    deserialize.name))


class CompositeField():
    def __init__(self, serialize=None, deserialize=None):
        self.serialize = serialize
        self.deserialize = deserialize


class Field():
    def __str__(self):
        return "(name: {0}, kind: {1})".format(
            self.name, self.kind)

    __repr__ = __str__


class DeserializeField(Field):
    '''DeserializeField
    name:
        name of the field that should be deserialized from, default is the
        name of the variable
    kind:
        the type of the variable should be deserialized to, default is what
        the deserialized variable is
    optional:
        specifies if the value is optional, if value is not found as a field
        the variable is left as None
    '''
    def __init__(self, name=None, kind=lambda x: x, optional=False):
        self.name = name
        self.kind = kind
        self.optional = optional

        if not callable(kind):
            raise Exception("Kind needs to be callable")


class SerializeField(Field):
    '''SerializeField
    name:
        name of the field that should serialize to, defaults to the variable
        name
    kind:
        the type that the field should be serialized to, defaults to the type
        that the variable is
    optional:
        specifies if the value is optional, if value is None then it will not
        get serialized
    '''
    def __init__(self, name=None, kind=lambda x: x, optional=False):
        self.name = name
        self.kind = kind
        self.optional = optional

        if not callable(kind):
            raise Exception("Kind needs to be callable")
