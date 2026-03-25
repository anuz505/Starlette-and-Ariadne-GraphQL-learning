from starlette.config import Config

config = Config("./app/.env")

DATABASE_URL = config("DATABASE_URL", cast=str)
HOST = config("HOST", cast=str, default="127.0.0.1")
PORT = config("PORT", cast=int, default=8000)
DEBUG = config("DEBUG", cast=bool, default=False)
APP_NAME = config("APP_NAME", cast=str, default="Task Manager API")
