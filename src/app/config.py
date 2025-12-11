from dataclasses import dataclass
from environs import Env


@dataclass
class BotEnv:
    token: str
    username: str

@dataclass
class WebEnv:
    n8n_url: str


@dataclass
class Config:
    tg_Bot: BotEnv
    web: WebEnv


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    
    return Config(
        tg_Bot=BotEnv(
            token=env("BOT_TOKEN"),
            username=env("BOT_USERNAME")
        ),
        web=WebEnv(
            n8n_url=env("N8N_SERVICE_ADDR")
        )
    )


