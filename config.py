from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VK_TOKEN: str
    GROUP_ID: int
    DATABASE_URL: str = "sqlite:///fitness_bot.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()