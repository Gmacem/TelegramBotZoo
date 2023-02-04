from aiohttp import ClientSession
from yarl import URL


class Client:
    def __init__(self, session: ClientSession, base_url: URL | str) -> None:
        if isinstance(base_url, str):
            base_url = URL(base_url)
        self.base_url: URL = base_url
        self.session: ClientSession = session
