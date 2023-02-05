import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql://Gmacem:HsKzHxv9R7Jn@rc1b-ch9xi0ktt03mpjpy.mdb.yandexcloud.net/EnCollectorDB")