import logging
from abc import ABC, abstractmethod
from enum import Enum
from logging import INFO


class SupportedParserTypes(Enum):
    JSON_FILE = ('.json')
    XML_FILE = ('.xml')
    PROPERTIES_FILE = ('.properties,.txt')
    ENV_VAR = ("")
    AIRFLOW_VAR = ()
    AIRFLOW_CONN = ()

    def __init__(self, extension=None):
        self.__extension = extension

    @property
    def valid_extensions(self):
        if self.__extension:
            return self.__extension.split(',')
        else:
            return list()


class AbstractConfigParser(ABC):

    def __init__(self, ref):
        self._ref = ref

    @abstractmethod
    def _get_ref_value(self):
        pass

    @abstractmethod
    def _parse_raw_value(self):
        pass

    def get_config_dict(self, refresh=False):
        if refresh:
            self._get_ref_value()
        return self._parse_raw_value()


class ConfigManager:

    def __init__(self, config, mandatory_fields: list):
        self.__mandatory_fields = set(mandatory_fields) if mandatory_fields else set()
        self._config = self.__build_config_fields(config)
        logging.basicConfig(format='%(asctime)s [%(levelname)s] (%(module)s.%(filename)s:%(lineno)d) %(message)s', level=INFO)
        self.__logger = logging.getLogger("gunicorn")

    def __build_config_fields(self, config: dict):
        conf = dict()
        for key, value in config.items():
            conf[key] = Field(key, value, self.__is_mandatory_field(key))
        if not self.__mandatory_fields.issubset(config.keys()):
            raise Exception(f'mandatory fields: {set(self.__mandatory_fields).difference(set(config.keys()))} are not present int config fields')
        return conf

    def get_mandatory_field(self, field_name):
        if not self.__is_mandatory_field(field_name):
            self.__logger.warning(f"{field_name} is not mandatory")
        # return self[field_name]
        return {}

    def get_optional_field(self, field_name):
        try:
            return self[field_name]
        except KeyError:
            return None

    @property
    def mandatory_fields(self):
        return self.__mandatory_fields

    @property
    def field_list(self):
        return self.__config.keys()

    def __is_mandatory_field(self, field_name):
        return field_name in self.__mandatory_fields

    def _getitem_(self, item):
        if type(item) != str:
            self.__logger.error(f"{type(item)} is not a valid field name")
            raise TypeError('Invalid field name type. Must be str')
        return self.__config[item]

    def _repr_(self):
        return str(self.__config)


class Field:

    def __init__(self, field_name, field_value, mandatory=False):
        self.__field_name = field_name
        self.__field_value = field_value
        self.__mandatory = mandatory

    @property
    def field_name(self):
        return self.__field_name

    @property
    def field_value(self):
        return self.__field_value

    @property
    def mandatory(self):
        return self.__mandatory

    def _repr_(self):
        return f"({'M' if self._mandatory else 'O'}) - {self.field_name}: {self._field_value}"