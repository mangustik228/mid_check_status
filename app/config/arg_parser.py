from configparser import ConfigParser
from typing import NamedTuple
import argparse
import sys


class _Args(NamedTuple):
    file_path: str
    debug: bool


def _get_version(config_path) -> str:
    _config_ini = ConfigParser()
    _config_ini.read(config_path)
    return _config_ini.get('default', 'version')


def get_namespace(config_path) -> _Args:
    parser = argparse.ArgumentParser(
        prog='',  # Название программы
        description='',
        epilog='Vasiliy mangust 2023'
    )
    version = _get_version(config_path)
    # параметр nargs:
    # "+" - 1 и более аргументов
    # "?" - 0 или 1 аргумент
    # Если не указывать: то 1

    parser.add_argument('file_path', nargs='?', default=False,
                        help='Путь до файла')

    parser.add_argument('-d', '--debug', action="store_true",
                        help='В режиме дебага')

    parser.add_argument('--version', action="version",
                        help='Вывести номер версии', version=f'%(prog)s {version}')

    namespace = parser.parse_args(sys.argv[1:])
    return namespace
