from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from configparser import ConfigParser
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

CONFIG_PATH = "config.ini"

_config_ini = ConfigParser()
_config_ini.read(CONFIG_PATH)


class _Telegram(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_")
    token: str
    ids_for_alert: str

    @property
    def ids(self):
        return [int(i) for i in self.ids_for_alert.split(',')]


class _Logs(BaseModel):
    rotation: str = _config_ini.get('logs', 'rotation')
    level: str = _config_ini.get('logs', 'level')
    telegram: bool = _config_ini.getboolean('logs', 'telegram')
    path: str = datetime.now().strftime('logs/%Y_%m_%d_log.log')


class _Parsing(BaseModel):
    url: str = _config_ini.get("parsing", "url")


class _Proxy(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROXY_")
    url: str
    token: int


class _Settings(BaseSettings):
    MODE: Literal['dev', "test", "prod"] = 'dev'
    logs: _Logs = _Logs()
    name: str = _config_ini.get('default', 'name')
    telegram: _Telegram = _Telegram()
    proxy: _Proxy = _Proxy()
    parsing: _Parsing = _Parsing()


settings = _Settings()
