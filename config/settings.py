from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings config

    This class is used to define the settings for the application.

    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    # DATABASE KEYS
    POSTGRES_USER: str = Field(validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(validation_alias="POSTGRES_DB")
    POSTGRES_PORT: str = Field(validation_alias="POSTGRES_PORT")
    POSTGRES_HOST: str = Field(validation_alias="POSTGRES_HOST")

    # BASE RPCs
    cdp_rpc: str = Field(validation_alias="CDP_RPC")
    ankr_rpc: str = Field(validation_alias="ANKR_RPC")
    blast_rpc: str = Field(validation_alias="BLAST_RPC")
    alchemy_rpc: str = Field(validation_alias="ALCHEMY_RPC")

    # ANCILLARY KEYS
    debank_api_key: str = Field(validation_alias="DEBANK_API_KEY")
    coin_gecko_api_key: str = Field(validation_alias="COIN_GECKO_API_KEY")
    base_scan_api_key: str = Field(validation_alias="BASE_SCAN_API_KEY")
    jina_api_key: str = Field(validation_alias="JINA_API_KEY")  # LLM SCRAPING API KEY


def get_postgres_uri(settings: Settings = Settings()) -> str:
    return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:5432/{settings.POSTGRES_DB}"
