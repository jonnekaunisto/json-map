import configparser


class ConfigBaseParent():
    def __init__(self):
        self._config_key_dict = {}

    def to_config(self, filename=None):
        config = configparser.ConfigParser()

        for field_name, field in self._config_key_dict.items():
            serialize = field.serialize
            if serialize is None:
                continue

            value = self.__dict__[field_name]
            if value is None and serialize.optional:
                continue

            value = serialize.kind(value)

            if not config.has_section(serialize.section):
                config.add_section(serialize.section)
            config.set(serialize.section, serialize.name, value)

        if filename is not None:
            with open(filename, 'w') as f:
                config.write(f)
        else:
            return config

    def from_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        for field_name, field in self._config_key_dict.items():
            deserialize = field.deserialize
            if deserialize is None:
                continue

            if not config.has_section(deserialize.section):
                raise Exception('{} section not found in the config'.format(
                    deserialize.section))

            if config.has_option(deserialize.section, deserialize.name):
                self.__dict__[field_name] = field.deserialize.kind(
                    config.get(deserialize.section, deserialize.name))
            elif not deserialize.optional:
                raise Exception('{} field not found in the config'.format(
                    deserialize.name))


class ConfigSectionBase(ConfigBaseParent):
    def __init__(self, section):
        super().__init__()
        self.section = section

    def init_deserialize_config(self):
        for field_name, field in self.__dict__.items():
            if type(field) is DeserializeConfigOption:
                if field.name is None:
                    field.name = field_name
                field.section = self.section

                if field_name in self._config_key_dict:
                    self._config_key_dict[field_name].deserialize = field
                else:
                    self._config_key_dict[field_name] = CompositeConfigOption(
                        deserialize=field)
                self.__dict__[field_name] = None

    def init_serialize_config(self):
        for field_name, field in self.__dict__.items():
            if type(field) is SerializeConfigOption:
                if field.name is None:
                    field.name = field_name
                field.section = self.section
                if field_name in self._config_key_dict:
                    self._config_key_dict[field_name].serialize = field
                else:
                    self._config_key_dict[field_name] = CompositeConfigOption(
                        serialize=field)
                self.__dict__[field_name] = None


class ConfigBase(ConfigBaseParent):
    def __init__(self):
        super().__init__()

    def init_deserialize_config(self):
        for field_name, field in self.__dict__.items():
            if type(field) is DeserializeConfigOption:
                if field.name is None:
                    field.name = field_name
                if field_name in self._config_key_dict:
                    self._config_key_dict[field_name].deserialize = field
                else:
                    self._config_key_dict[field_name] = CompositeConfigOption(
                        deserialize=field)
                self.__dict__[field_name] = None

    def init_serialize_config(self):
        for field_name, field in self.__dict__.items():
            if type(field) is SerializeConfigOption:
                if field.name is None:
                    field.name = field_name

                if field_name in self._config_key_dict:
                    self._config_key_dict[field_name].serialize = field
                else:
                    self._config_key_dict[field_name] = CompositeConfigOption(
                        serialize=field)
                self.__dict__[field_name] = None


class CompositeConfigOption():
    def __init__(self, serialize=None, deserialize=None, is_section=False):
        self.serialize = serialize
        self.deserialize = deserialize
        self.is_section = is_section

    def __str__(self):
        return "serialize: {} deserialize: {}".format(self.serialize,
                                                      self.deserialize)

    __repr__ = __str__


class ConfigField():
    def __str__(self):
        return "(section {0} name: {1}, kind: {2}, optional: {3})".format(
            self.section, self.name, self.kind, self.optional)

    __repr__ = __str__


class SerializeConfigOption(ConfigField):
    def __init__(self, name=None, section=None, kind=str,
                 optional=False):
        self.name = name
        self.section = section
        self.kind = kind
        self.optional = optional


class DeserializeConfigOption(ConfigField):
    def __init__(self, name=None, section=None, kind=lambda x: x,
                 optional=False):
        self.name = name
        self.section = section
        self.kind = kind
        self.optional = optional
