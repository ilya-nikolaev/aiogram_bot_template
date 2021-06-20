from environs import Env
from dataclasses import dataclass


@dataclass
class BotSettings:
    token: str
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
    env = Env()
    env.read_env()
    
    return Config(
        bot_settings=BotSettings(
            token=env.str("TG_BOT_TOKEN"),
            use_redis=env.bool("USE_REDIS")
        ),
        db_settings=DBSettings(
            host=env.str("DB_HOST"),
            name=env.str("DB_NAME"),
            user=env.str("DB_USER"),
            pswd=env.str("DB_PSWD"),
        )
    )
