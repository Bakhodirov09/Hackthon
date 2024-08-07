import pytz
import datetime
from environs import Env
from environs import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

load_dotenv('.env')
env = Env()

BASE_DIR = Path(__file__).resolve().parent.parent

DOMAIN = env.str("DOMAIN")

class PostgresSettings(BaseSettings):
    name: str
    user: str
    password: str
    host: str
    port: int
    
    @property
    def url(self) -> str:
        psql = f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        return f"postgresql://{psql}"

    model_config = SettingsConfigDict(env_prefix='db_', env_file=f'{BASE_DIR}/.env', extra='allow')


class DjangoSettings(BaseSettings):
    secret_key: str
    debug: bool
    allowed_hosts: str
    csrf_trusted_origins: str
    
    @property
    def csrf_trusted_origins_list(self) -> list:
        return [origin.strip() for origin in self.csrf_trusted_origins.split(",") if origin.strip()]
    
    @property
    def allowed_hosts_list(self) -> list:
        return [allowed_host.strip() for allowed_host in self.allowed_hosts.split(",") if allowed_host.strip()]

    model_config = SettingsConfigDict(env_prefix='django_', env_file=f'{BASE_DIR}/.env', extra='allow')


class BotSettings(BaseSettings):
    token: str
    name: str
    admins: str
    web_app_url: str

    model_config = SettingsConfigDict(env_prefix='bot_', env_file=f'{BASE_DIR}/.env', extra='allow')

    @property
    def bot_admins(self) -> list:
        return [int(admin.strip()) for admin in self.admins.split(",") if admin.strip()]


tashkent_tz = pytz.timezone('Asia/Tashkent')
utc = pytz.utc

def current_time(time_zone: bool = False):
    return datetime.datetime.now(tz = (tashkent_tz if time_zone else utc))