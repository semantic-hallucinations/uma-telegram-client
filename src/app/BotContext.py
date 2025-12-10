from typing import Dict

from aiogram import Router


class BotContext:
    _username: str
    _router_map: dict

    @property
    def username(self) -> str:
        username = self._username
        return username.lstrip('@') if username.startswith('@') else username

    @property
    def tagged_username(self) -> str:
        tagged = self._username
        return tagged if tagged.startswith('@') else f"{tagged}"

    @property
    def routers(self) -> Dict[Router]:
        return self._route_map