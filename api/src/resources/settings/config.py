from pyconfs import Configuration
from pathlib import Path
from os import getenv, path


project_root = Path(__file__).parent.parent.parent
toml_path = path.join(project_root, "pyproject.toml")
cf = Configuration.from_file(toml_path)


class Settings:
    def __init__(self) -> None:

        # global variables for mysql
        self.sql_host: str = ""
        self.sql_port: int = 0
        self.sql_db: str = ""
        self.sql_username: str = ""
        self.sql_password: str = ""
        self.db_url: str = ""

        # Api
        self.log_type: str = ""
        self.host_url: str = ""
        self.debug: bool = False
        self.auth_type: str = ""

        self.pwd_len: int = 0
        self.round: int = 0
        self.coding: str = ""

        # global variables for RabbitMQ
        self.rabbit_host_name: str = ""
        self.rabbit_host_port: str = ""
        self.rabbit_connect_string: str = ""
        self.queue_name: list = []

        # Project details
        self.name: str = ""
        self.version: str = ""
        self.description: str = ""

        # JWT params
        self.algorithm: str = ""
        self.secret_key: str = ""
        self.token_url: str = ""
        self.grant_type: str = ""
        self.token_expire_min: int = 0
        self.refresh_token_expire_minutes: int = 0

        # Google AUTH
        self.google_client_secret: str = ""
        self.google_client_id: str = ""
        # News
        self.news_api_key: str = ""
        # admin
        self.email: str = ""
        self.password: str = ""
        self.username: str = ""
        self.is_admin: bool = True
        self.telephone: int = 0

    def from_toml_file(self):
        self.sql_host = cf.database.host
        self.sql_port = cf.database.port
        self.sql_db = cf.database.db
        self.sql_username = cf.database.user
        self.sql_password = cf.database.pwd
        self.db_url = f"mariadb+asyncmy://{self.sql_username}:{self.sql_password}@{self.sql_host}/{self.sql_db}?charset=utf8mb4"

        self.rabbit_host_name = cf.queue.params.host_name
        self.rabbit_host_port = cf.queue.params.port
        self.queue_name = cf.queue.params.my_queue
        self.rabbit_connect_string: str = (
            "amqp://guest:guest@"
            + self.rabbit_host_name
            + ":"
            + self.rabbit_host_port
            + "/"
        )
        self.log_type = cf.api.log_type
        self.host_url = cf.api.host_url
        self.debug = cf.api.debug
        self.auth_type = cf.api.auth_type

        self.google_client_id = cf.api.google_client_id

        self.pwd_len = cf.hash.password.length
        self.rounds = cf.hash.password.rounds
        self.coding = cf.hash.password.coding

        self.name = cf.elyte.api.app["name"]
        self.version = cf.tool.poetry.version
        self.description = cf.elyte.api.app.description

        self.algorithm = cf.token.params.algorithm
        self.secret_key = cf.token.params.secret_key
        self.token_expire_min = cf.token.params.token_expire_min
        self.refresh_token_expire_minutes = (
            cf.token.params.refresh_token_expire_minutes
        )
        self.grant_type = cf.token.params.grant_type
        self.news_api_key = cf.api.news_api_key

        self.email = cf.admin.email
        self.password = cf.admin.password
        self.username = cf.admin.username
        self.telephone = cf.admin.telephone
        return self

    def from_env_file(self):

        print("Overriding  variables for FastAPI, MySQL")

        self.sql_port = str(getenv("MYSQL_HOST"))
        self.sql_db = str(getenv("MYSQL_DATABASE"))
        self.sql_username = str(getenv("MYSQL_USER"))
        self.sql_password = str(getenv("MYSQL_ROOT_PASSWORD"))

        self.google_client_id = str(getenv("GOOGLE_CLIENT_ID"))
        self.secret_key = str(getenv("SECRET_KEY"))
        self.host_url = str(getenv("HOST_URL"))

        self.token_expire_min = int(getenv("TOKEN_EXPIRE_MINUTES"))
        self.algorithm = str(getenv("ALGORITHM"))

        return self
