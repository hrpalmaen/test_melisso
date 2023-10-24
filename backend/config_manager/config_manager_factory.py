import pathlib

from backend.config_manager.config_manager import SupportedParserTypes, ConfigManager
from backend.config_manager.parser.basic_parsers import EnvVarConfigParser, JsonFileConfigParser, PropertiesFileConfigParser, XMLFileConfigParser


class ConfigManagerFactory:
    __PARSERS = {
        SupportedParserTypes.ENV_VAR: EnvVarConfigParser,
        SupportedParserTypes.JSON_FILE: JsonFileConfigParser,
        SupportedParserTypes.PROPERTIES_FILE: PropertiesFileConfigParser,
        SupportedParserTypes.XML_FILE: XMLFileConfigParser
    }

    @staticmethod
    def get_instance(config_type: SupportedParserTypes, config_ref: str, mandatory_fields: list = None, **kwargs):
        if config_type.valid_extensions and pathlib.Path(config_ref).suffix not in config_type.valid_extensions:
            raise TypeError(f'extension {pathlib.Path(config_ref).suffix} is not supported for parser {config_type.name}. Valid extension are: {config_type.valid_extensions}')
        return ConfigManager(config=ConfigManagerFactory.__PARSERS.get(config_type)(config_ref, **kwargs).get_config_dict(),
                             mandatory_fields=mandatory_fields)