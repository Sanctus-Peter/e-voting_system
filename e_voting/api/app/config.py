from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_username: str
    db_name: str
    secret_key: str
    algorithm: str
    access_tok_expire_minutes: int

    class Config:
        env_file = "C:\\Users\\MAHADI\\Documents\\Python Projects\\e-voting_system\\e_voting\\api\\.env"


settings = Settings()
