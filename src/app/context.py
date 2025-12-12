from dataclasses import dataclass
from config import load_config

@dataclass
class BotContext:
    _username: str

    @property
    def username(self) -> str:
        username = self._username
        return username.lstrip('@') if username.startswith('@') else username

    @property
    def tagged_username(self) -> str:
        tagged = self._username
        return tagged if tagged.startswith('@') else f"@{tagged}"


@dataclass
class WebContext:
    n8n_url: str




_cfg = load_config()

bot_context = BotContext(_cfg.tg_Bot.username)
web_context = WebContext(_cfg.web.n8n_url)