import json
import os


from backend.config_manager.config_manager import AbstractConfigParser


class EnvVarConfigParser(AbstractConfigParser):

    def __init__(self, ref: str, parsing_type: str = 'simple', allow_none: bool = True):
        super().__init__(ref)
        self.__parsing_type = parsing_type
        self.__allow_none = allow_none
        self.__raw_value = None
        self._get_ref_value()

    def _get_ref_value(self):
        value = os.environ.get(self._ref)
        if not self.__allow_none and not value:
            raise ValueError(f'Env Var {self._ref} is not set')
        self.__raw_value = value

    def _parse_raw_value(self):
        if self.__parsing_type.lower() == 'simple':
            return {self._ref: self.__raw_value}
        elif self.__parsing_type.lower() == 'json':
            return json.loads(self.__raw_value)
        else:
            raise TypeError(f'Unsupported parsing type {self.__parsing_type}')


class JsonFileConfigParser(AbstractConfigParser):

    def __init__(self, ref):
        super().__init__(ref)
        self.__raw_value = None
        self._get_ref_value()

    def _get_ref_value(self):
        self.__raw_value = open(self._ref)

    def _parse_raw_value(self):
        return json.load(self.__raw_value)

    def _del_(self):
        self.__raw_value.close()


class XMLFileConfigParser(AbstractConfigParser):
    def __init__(self, ref):
        super().__init__(ref)
        self.__raw_value = None
        self._get_ref_value()

    def _get_ref_value(self):
        self.__raw_value = open(self._ref)

    def _parse_raw_value(self):
        # return xmltodict.parse(self.__raw_value.read())
        return {}

    def _del_(self):
        self.__raw_value.close()


class PropertiesFileConfigParser(AbstractConfigParser):
    def __init__(self, ref):
        super().__init__(ref)
        self.__raw_value = None
        self._get_ref_value()

    def _get_ref_value(self):
        self.__raw_value = open(self._ref)

    def _parse_raw_value(self):
        lines = self.__raw_value.readlines()
        return {key: value for key, value in filter(None, [self.__parse_line(line) for line in lines])}

    def __parse_line(self, line):
        line = line.strip()
        if not line:
            return None
        elif line.startswith('#'):
            return None
        else:
            line_tokens = line.split('#')
            if len(line_tokens) > 1:
                return self.__parse_line(line_tokens[0])
            else:
                line_tokens = line.split('=')
                return line_tokens[0], line_tokens[1]

    def _del_(self):
        self.__raw_value.close()