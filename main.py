
from backend.config_manager.config_manager import SupportedParserTypes
from backend.config_manager.config_manager_factory import ConfigManagerFactory
from backend.connection_manager import ConnectionManager

from fastapi import FastAPI
# from admin.sec import users_urls
# from middleware import main_middleware

app = FastAPI()

# app.include_router(users_urls.router)


def get_db_values(prefix: str):
    vals = dict()
    # vals['host'] = (
    #     ConfigManagerFactory.get_instance(SupportedParserTypes.ENV_VAR, f'{prefix}_HOST', [f'{prefix}_HOST'])
    #     .get_mandatory_field(f'{prefix}_HOST')
    #     .field_value
    # )
    # vals['db_name'] = (
    #     ConfigManagerFactory.get_instance(SupportedParserTypes.ENV_VAR, f'{prefix}_NAME', [f'{prefix}_NAME'])
    #     .get_mandatory_field(f'{prefix}_NAME')
    #     .field_value
    # )
    # vals['user'] = (
    #     ConfigManagerFactory.get_instance(SupportedParserTypes.ENV_VAR, f'{prefix}_USER', [f'{prefix}_USER'])
    #     .get_mandatory_field(f'{prefix}_USER')
    #     .field_value
    # )
    # vals['password'] = (
    #     ConfigManagerFactory.get_instance(SupportedParserTypes.ENV_VAR, f'{prefix}_PASSW', [f'{prefix}_PASSW'])
    #     .get_mandatory_field(f'{prefix}_PASSW')
    #     .field_value
    # )
    # vals['port'] = (
    #     ConfigManagerFactory.get_instance(SupportedParserTypes.ENV_VAR, f'{prefix}_PORT')
    #     .get_optional_field(f'{prefix}_PORT')
    #     .field_value
    # )
    vals['host'] = 'localhost'
    vals['db_name'] = 'ruteando'
    vals['user'] = 'postgres'
    vals['password'] = 'postgres'
    vals['port'] = '5432'
    return vals


def init_dbs(conn_manager: ConnectionManager = ConnectionManager.get_instance()):
    conn_manager.get_connection('postgresql', 'main_db', **get_db_values('ruteando_db'))


init_dbs()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
