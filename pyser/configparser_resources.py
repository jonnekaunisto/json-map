import configparser


class ConfigBaseParent():
    def __init__(self):
        self._config_key_dict = {}

    # TODO: add checks for if filename is valid
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

            if type(field) is CompositeConfigOption:
                if config.has_option(deserialize.section, deserialize.name):
                    self.__dict__[field_name] = field.deserialize.kind(
                        config.get(deserialize.section, deserialize.name))
                elif not config.has_section(deserialize.section) and not deserialize.optional:
                    raise Exception('"{}" section not in config'.format(
                        deserialize.section))
                elif not deserialize.optional:
                    raise Exception('"{}" option not in config'.format(
                        deserialize.name))
            elif type(field) is CompositeConfigSection:
                self.__dict__[field_name].from_config(filename)


class ConfigSectionBase(ConfigBaseParent):
    '''ConfigSectionBase
    '''
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

    def __set_serialize_section__(self, section):
        for field in self._config_key_dict.values():
            if field.serialize is not None:
                field.serialize.section = section

    def __set_deserialize_section__(self, section):
        for field in self._config_key_dict.values():
            if field.deserialize is not None:
                field.deserialize.section = section


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
            elif type(field) is DeserializeConfigSection:
                if field_name in self._config_key_dict:
                    self._config_key_dict[field_name].deserialize = field
                else:
                    self._config_key_dict[field_name] = CompositeConfigSection(
                        deserialize=field)

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
            elif type(field) is SerializeConfigSection:
                if field_name in self._config_key_dict:
                    self._config_key_dict[field_name].serialize = field
                else:
                    self._config_key_dict[field_name] = CompositeConfigSection(
                        serialize=field)

    def init_section_values(self):
        for field_name, field in self._config_key_dict.items():
            if type(field) is CompositeConfigSection:
                target = self.__dict__[field_name]
                if field.serialize is not None:
                    target.__set_serialize_section__(field.serialize.section)
                if field.deserialize is not None:
                    target.__set_deserialize_section__(field.deserialize.section)


class CompositeConfigOption():
    def __init__(self, serialize=None, deserialize=None, is_section=False):
        self.serialize = serialize
        self.deserialize = deserialize

    def __str__(self):
        return "serialize: {} deserialize: {}".format(self.serialize,
                                                      self.deserialize)

    __repr__ = __str__


class ConfigOption():
    def __str__(self):
        return "(section {0} name: {1}, kind: {2}, optional: {3})".format(
            self.section, self.name, self.kind, self.optional)

    __repr__ = __str__


class SerializeConfigOption(ConfigOption):
    def __init__(self, name=None, section=None, kind=str,
                 optional=False):
        self.name = name
        self.section = section
        self.kind = kind
        self.optional = optional


class DeserializeConfigOption(ConfigOption):
    def __init__(self, name=None, section=None, kind=lambda x: x,
                 optional=False):
        self.name = name
        self.section = section
        self.kind = kind
        self.optional = optional


class CompositeConfigSection():
    def __init__(self, serialize=None, deserialize=None, is_section=False):
        self.serialize = serialize
        self.deserialize = deserialize

    def __str__(self):
        return "serialize: {} deserialize: {}".format(self.serialize,
                                                      self.deserialize)

    __repr__ = __str__


class ConfigSection():
    def __str__(self):
        return "(section {0} optional: {1})".format(
            self.section, self.optional)

    __repr__ = __str__


class SerializeConfigSection(ConfigSection):
    def __init__(self, section, optional=False):
        self.section = section
        self.optional = optional


class DeserializeConfigSection(ConfigSection):
    def __init__(self, section, optional=False):
        self.section = section
        self.optional = optional
