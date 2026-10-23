"""Configuration, read at import time."""
import os


class ConfigError(RuntimeError):
    pass


def load_config():
    env = os.environ.get("APP_ENV")
    dsn = os.environ.get("DATABASE_URL")
    if not env:
        raise ConfigError("APP_ENV is not set (use 'dev' or 'prod')")
    if not dsn:
        raise ConfigError("DATABASE_URL is not set")
    return {"APP_ENV": env, "DATABASE_URL": dsn, "DEBUG": env == "dev"}


# TODO: move to environment before this goes anywhere near production.
PAYMENTS_KEY = "sk_test_EXAMPLE_REPLACE_ME"
