import argparse
import shutil
import configparser
import sys
from os import walk, mkdir, listdir, remove, rmdir
from os.path import join, exists, split, isfile, isdir


# =================Для вызова скрипта из консоли с параметрами.
parser = argparse.ArgumentParser(description='Указание директории искточника, директории назначения '
                                             'и настроек БД в sbis-rpc-service.ini.')
parser.add_argument('-s', '--source', required=True, action='store', dest='source', type=str, metavar='',
                    help='Директория, содержащая файлы\папки для копирования.')
parser.add_argument('-d', '--destination', required=True, action='store', dest='destination', type=str, metavar='',
                    help='Директория, в которую будет скопирована директория источника.')
parser.add_argument('-dbh', '--db_host', action='store', dest='db_host', type=str, default='localhost', metavar='')
parser.add_argument('-dbp', '--db_port', action='store', dest='db_port', type=str, default='5432', metavar='')
parser.add_argument('-dbn', '--db_name', action='store', dest='db_name', type=str, default='unittests_DB_2', metavar='')
parser.add_argument('-dbu', '--db_user', action='store', dest='db_user', type=str, default='postgres', metavar='')
parser.add_argument('-dbpsw', '--db_password', action='store', dest='db_password', type=str, default='postgres', metavar='')
results = parser.parse_args()

# =================Глобальные переменные.
MODULE_NAMES = ['Python', 'Бизнес-логика', 'Работа с БД']  # Необходимые модули платформы для прогонки тестов C++\Python API.
SOUR_DIR = results.source
SOUR_MODULES_DIR = join(SOUR_DIR, 'www\service\Модули')
DEST_DIR = results.destination
DEST_PLATF_DIR = join(DEST_DIR, split(SOUR_DIR)[1])
DEST_MODULES_DIR = join(DEST_PLATF_DIR, 'www\service\Модули')

DB_SETTINGS = dict(
    DB_HOST = results.db_host,
    DB_PORT = results.db_port,
    DB_NAME = results.db_name,
    DB_USER = results.db_user,
    DB_PASSWORD = results.db_password
    )

# =================Удаление старого каталога.
def removeall(path, recursion=True):
    if isdir(path):
        if len(listdir(path)) > 0:
            for name in listdir(path):
                joined_path = join(path, name)
                if isfile(joined_path): remove(joined_path)
                if isdir(joined_path):
                    removeall(joined_path)
            if recursion: removeall(path, False)
        else: rmdir(path)

if exists(DEST_PLATF_DIR):
    removeall(DEST_PLATF_DIR)

# =================Копирование обновлённого каталога.
for dirpath, dirnames, filenames in walk(SOUR_DIR):
    joined_dir = join(DEST_PLATF_DIR, dirpath.replace(SOUR_DIR, '').lstrip('\\'))  # Текущая директория для
                                                                                   # ЛОКАЛЬНОГО диска.
    # Сперва проверка на директорию модулей платформы, чтобы создать папки\файлы модулей только из MODULE_NAMES.
    if SOUR_MODULES_DIR.lower() in dirpath.lower():
        if not exists(DEST_MODULES_DIR): mkdir(DEST_MODULES_DIR)
        for module_name in MODULE_NAMES:
            if module_name.lower() in dirpath.lower():
                if not exists(joined_dir): mkdir(joined_dir)
                for filename in filenames:
                    shutil.copy2(join(dirpath, filename), joined_dir)
    # Для остальных верхних папок копируем всё, без архива jinnee.zip.
    else:
        mkdir(joined_dir)
        for filename in filenames:
            if filename == 'jinnee.zip' or filename == 'jinnee_lite.zip':
                continue
            shutil.copy2(join(dirpath, filename), joined_dir)

# =================После копирования платформы, необходимо отредактированть настройку подключения к БД.
rpc_serv_conf = configparser.ConfigParser()
rpc_serv_conf.optionxform = lambda opt: opt  # Для того, чтобы регистр строк параметров не изменялся при перезиписи.
rpc_serv_dir = join(split(DEST_MODULES_DIR)[0], 'sbis-rpc-service.ini')

with open(rpc_serv_dir) as f:
    rpc_serv_conf.read_file(f)
    settings = "postgresql: host='{DB_HOST}' port='{DB_PORT}' dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}'"
    settings = settings.format_map(DB_SETTINGS)
    rpc_serv_conf.set('Базовая конфигурация', 'БазаДанных', settings)

with open(rpc_serv_dir, 'w') as f:
    rpc_serv_conf.write(f)