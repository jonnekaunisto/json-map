import configparser


class ConfigSectionBase():
    def __init__(self, section):
        self.__config_key_dict = {}
        self.section = section

    def init_deserialize_config(self):
        for field_name, field in self.__dict__.items():
            if type(field) is DeserializeConfigOption:
                if field.name is None:
                    field.name = field_name

                if field_name in self.__config_key_dict:
                    self.__config_key_dict[field_name].deserialize = field
                else:
                    self.__config_key_dict[field_name] = CompositeConfigOption(
                        deserialize=field)
                self.__dict__[field_name] = None

    def from_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)

        if not config.has_section(self.section):
            raise Exception('{} section not in config'.format(self.section))

        for field_name, field in self.__config_key_dict.items():
            deserialize = field.deserialize

            if config.has_option(deserialize.section, deserialize.name):
                self.__dict__[deserialize.name] = field.deserialize.kind(
                    config.get(self.section, deserialize.name))
            elif not deserialize.optional:
                raise Exception('{} field not found in the json'.format(
                    deserialize.name))


class ConfigBase():
    def __init__(self):
        self.__config_key_dict = {}

    def init_deserialize_config(self):
        for field_name, field in self.__dict__.items():
            if type(field) is DeserializeConfigOption:
                if field.name is None:
                    field.name = field_name

                if field_name in self.__config_key_dict:
                    self.__config_key_dict[field_name].deserialize = field
                else:
                    self.__config_key_dict[field_name] = CompositeConfigOption(
                        deserialize=field)
                self.__dict__[field_name] = None

    def from_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)

        for field_name, field in self.__config_key_dict.items():
            deserialize = field.deserialize

            if config.has_option(deserialize.section, deserialize.name):
                self.__dict__[deserialize.name] = field.deserialize.kind(
                    config.get(deserialize.section, deserialize.name))
            elif not deserialize.optional:
                raise Exception('{} field not found in the json'.format(
                    deserialize.name))


class CompositeConfigOption():
    def __init__(self, serialize=None, deserialize=None):
        self.serialize = serialize
        self.deserialize = deserialize


class SerializeConfigOption():
    def __init__(self, name=None, section=None, kind=lambda x: x,
                 optional=False):
        self.name = name
        self.section = section
        self.kind = kind
        self.optional = optional


class DeserializeConfigOption():
    def __init__(self, name=None, section=None, kind=lambda x: x,
                 optional=False):
        self.name = name
        self.section = section
        self.kind = kind
        self.optional = optional
