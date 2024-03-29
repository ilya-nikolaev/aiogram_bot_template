from dataclasses import dataclass
from os import getenv

from config.utils import str_to_bool, int_list_from_str


@dataclass
class BotSettings:
    token: str
    admins: list[int]
    use_redis: bool


@dataclass
class DBSettings:
    name: str
    user: str
    pswd: str
    host: str
    port: str = "5432"


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
            port=getenv("DB_PORT"),
            name=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            pswd=getenv("DB_PSWD"),
        )
    )
