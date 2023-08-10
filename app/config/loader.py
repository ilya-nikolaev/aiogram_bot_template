from dataclasses import dataclass
from os import getenv

from app.config.utils import str_to_bool, int_list_from_str


@dataclass
class BotSettings:
    token: str
    admins: list[int]
    use_redis: bool


@dataclass
class DBSettings:
    host: str
    name: str
    user: str
    pswd: str


@dataclass
class Config:
    bot_settings: BotSettings
    db_settings: DBSettings


def load_config() -> Config:
    return Config(
        bot_settings=BotSettings(
            token=getenv("TG_BOT_TOKEN"),
            use_redis=str_to_bool(getenv("USE_REDIS")),
            admins=int_list_from_str(getenv("ADMINS"))
        ),
        db_settings=DBSettings(
            host=getenv("DB_HOST"),
            name=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            pswd=getenv("DB_PSWD")
        )
    )
