from dataclasses import dataclass

from environs import Env


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
    env = Env()
    
    return Config(
        bot_settings=BotSettings(
            token=env.str("TG_BOT_TOKEN"),
            use_redis=env.bool("USE_REDIS"),
            admins=[int(admin_id) for admin_id in env.list("ADMINS")]
        ),
        db_settings=DBSettings(
            host=env.str("DB_HOST"),
            name=env.str("DB_NAME"),
            user=env.str("DB_USER"),
            pswd=env.str("DB_PSWD"),
        )
    )
