import logging

class EnvKeysConsts:
    BOT_TOKEN = "BOT_TOKEN"
    LOG_LEVEL = "LOG_LEVEL"
    LOG_LEVEL_DEFALUT_VALUE = logging.ERROR
    BASE_FILE_URL = "BASE_FILE_URL"
    BASE_FILE_URL_DEFAULT_VALUE = "https://api.telegram.org/file/bot"
    API_BASE_URL = "API_BASE_URL"
    API_BASE_URL_DEFAULT_VALUE = "https://api.telegram.org/bot"
    READ_TIMEOUT = "READ_TIMEOUT"
    READ_TIMEOUT_DEFAULT_VALUE = 5.0
    QBITTORENT_URL = "QBITTORENT_URL"
    QBITTORENT_USERNAME = "QBITTORENT_USERNAME"
    QBITTORENT_PASSWORD = "QBITTORENT_PASSWORD"
    IS_LOCAL_API = "IS_LOCAL_API"
    IS_LOCAL_API_DEFAULT_VALUE = False
    EXTERNAL_MEMORY_PATH = "EXTERNAL_MEMORY_PATH"