from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MASTER_DATABASE_URL: str
    REPLICA_DATABASE_URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

settings = Settings()
