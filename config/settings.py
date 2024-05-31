from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings config

    Attributes:
        debank_api_key (str): Debank API key
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    POSTGRES_USER: str = Field(validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(validation_alias="POSTGRES_DB")
    POSTGRES_PORT: str = Field(validation_alias="POSTGRES_PORT")
    POSTGRES_HOST: str = Field(validation_alias="POSTGRES_HOST")
    debank_api_key: str = Field(validation_alias="DEBANK_API_KEY")
    base_api_key: str = Field(validation_alias='BASE_API_KEY')
    base_rpc: str = Field(validation_alias='BASE_HTTPS_URL')
    base_websocket: str = Field(validation_alias='BASE_WEBSOCKET_URL')
    account_pk: str = Field(validation_alias='ACCOUNT_1_PK')
    jina_api_key : str = Field(validation_alias='JINA_API_KEY')
    coin_gecko_api_key : str = Field(validation_alias='COIN_GECKO_API_KEY')

def get_postgres_uri(settings: Settings = Settings()) -> str:
    return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:5432/{settings.POSTGRES_DB}"
