import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv(
    "CONNECTION_STRING",
    "postgresql://Gmacem:HsKzHxv9R7Jn@rc1b-ch9xi0ktt03mpjpy.mdb.yandexcloud.net/EnCollectorDB",
)

CLIENTS_YA_TRANSLATOR_IAM_TOKEN: str = os.getenv("CLIENTS_YA_TRANSLATOR_IAM_TOKEN")
CLIENTS_YA_TRANSLATOR_FOLDER_ID: str = os.getenv("CLIENTS_YA_TRANSLATOR_FOLDER_ID")
CLIENTS_YA_TRANSLATOR_BASE_URL: str = os.getenv(
    "CLIENTS_YA_TRANSLATOR_BASE_URL", "https://translate.api.cloud.yandex.net"
)

CLIENTS_YA_DICTIONARY_API_KEY: str = os.getenv("CLIENTS_YA_DICTIONARY_API_KEY")
CLIENTS_YA_DICTIONARY_BASE_URL: str = os.getenv(
    "CLIENTS_YA_DICTIONARY_BASE_URL", "https://dictionary.yandex.net"
)

BOTS_ENCOLLECTOR_TOKEN: str = os.getenv("BOTS_ENCOLLECTOR_TOKEN", "TOKEN")

BASE_URL: str = os.getenv("BASE_URL")
ADMIN_CHAT_ID: str = os.getenv("ADMIN_CHAT_ID", "12345")
PORT: str = os.getenv("PORT", "8443")
CERTIFICATE_PATH: str = os.getenv("CERTIFICATE_PATH")
SOURCE: str = os.getenv("SOURCE")
