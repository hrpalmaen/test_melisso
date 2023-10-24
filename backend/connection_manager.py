from enum import Enum

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker


class SupportedDBEngine(Enum):
    POSTGRESQL = ('postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}', '5432')
    MONGODB = ('mongodb:///?Server={host}&Port={port}&Database={db_name}&User={user}&Password={password}', '27017')

    def __init__(self, conn_string, default_port):
        self.conn_string = conn_string
        self.default_port = default_port

    def build_conn_string(self, **kwargs):
        if not kwargs.get('port'):
            kwargs['port'] = self.default_port
        return self.conn_string.format(**kwargs)

    def get_conn_parameters(self, **kwargs):
        if not kwargs.get('port'):
            kwargs['port'] = self.default_port
        return {
            'user': kwargs.get('user'),
            'password': kwargs.get('password'),
            'host': kwargs.get('host'),
            'db_name': kwargs.get('db_name'),
            'port': kwargs.get('port'),
        }

    @staticmethod
    def get_engine_by_type_name(type_name: str):
        types = {
            SupportedDBEngine.POSTGRESQL.name: SupportedDBEngine.POSTGRESQL,
            SupportedDBEngine.MONGODB.name: SupportedDBEngine.MONGODB,
        }
        return types.get(type_name.upper()) if type_name is not None else None


class ConnectionManager:
    __INSTANCE = None

    def __init__(self):
        self.__available_connections = dict()
        self.__default_conn_name = None
        self.__params_connections = dict()

    @staticmethod
    def get_instance():
        if not ConnectionManager.__INSTANCE:
            ConnectionManager.__INSTANCE = ConnectionManager()
        return ConnectionManager.__INSTANCE

    def get_connection(self, conn_type: str, conn_name: str, **kwargs):
        conn = self.get_conn_by_name(conn_name)
        is_default = True if not self.__available_connections else kwargs.get('set_default', False)
        force_replace = kwargs.get('force_replace', False)
        if not conn or force_replace:
            if force_replace:
                self.release_connection(conn_name)
            conn_type = SupportedDBEngine.get_engine_by_type_name(conn_type)
            conn = sql.create_engine(conn_type.build_conn_string(**kwargs))
            self.__params_connections = conn_type.get_conn_parameters(**kwargs)
            self.__available_connections[conn_name] = conn
        if is_default:
            self.__default_conn_name = conn_name
        return conn

    def get_conn_by_name(self, conn_name=None):
        if not conn_name:
            conn_name = self.__default_conn_name
        return self.__available_connections.get(conn_name)

    def get_orm_session(self, conn_name=None):
        session_class = sessionmaker()
        session_class.configure(bind=self.get_conn_by_name(conn_name))
        return session_class()

    def release_connection(self, conn_name):
        conn = self.get_conn_by_name(conn_name)
        if conn:
            conn.dispose()
            del self.__available_connections[conn_name]

    @property
    def conns(self):
        return self.__available_connections.keys()

    def get_params_connection(self, schema, pool_size: int = 10):
        return self.__params_connections