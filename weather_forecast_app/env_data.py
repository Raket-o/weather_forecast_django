"""Модуль конфиг для проверки создано ли окружение."""
import os

from dotenv import find_dotenv, get_cli_string, load_dotenv

get_cli_string(path="../.env")

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = "192.168.55.4"
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
debug = os.getenv("DEBUG").capitalize()
log_level = os.getenv("LOG_LEVEL").upper()
login_superuser = os.getenv("LOGIN_SUPERUSER")
