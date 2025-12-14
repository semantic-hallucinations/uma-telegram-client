from dataclasses import dataclass
from config import load_config

from aiogram.enums import ParseMode

@dataclass
class BotContext:
    _username: str
    _parse_mode_map = {
        "DEFAULT" : None,
        "MARKDOWN" : ParseMode.MARKDOWN,
        "MARKDOWN_V2" : ParseMode.MARKDOWN_V2,
        "HTML" : ParseMode.HTML
    }

    @property
    def username(self) -> str:
        username = self._username
        return username.lstrip('@') if username.startswith('@') else username

    @property
    def tagged_username(self) -> str:
        tagged = self._username
        return tagged if tagged.startswith('@') else f"@{tagged}"
    
    @property
    def supported_parse_modes(self) -> ParseMode | None:
        return self._parse_mode_map



@dataclass
class WebContext:
    n8n_url: str
    n8n_answer_format: str




_cfg = load_config()

bot_context = BotContext(_cfg.tg_Bot.username)
web_context = WebContext(
    _cfg.web.n8n_url,
    _cfg.web.n8n_answer_format
)

