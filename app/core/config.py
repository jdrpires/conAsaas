from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    asaas_api_key: str
    asaas_base_url: str = "https://sandbox.asaas.com/api/v3"
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    return Settings()
