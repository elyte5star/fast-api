from pyconfs import Configuration
from pathlib import Path
from os import getenv, path
from fastapi_mail import ConnectionConfig
from typing import Any
import secrets


project_root = Path(__file__).parent.parent.parent
toml_path = path.join(project_root, "pyproject.toml")
cf = Configuration.from_file(toml_path)
import json


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
        self.origins: list[str] = ["*"]

        self.pwd_len: int = 0
        self.round: int = 0
        self.encoding: str = ""

        # global variables for RabbitMQ
        self.rabbit_host_name: str = ""
        self.rabbit_host_port: str = ""
        self.rabbit_connect_string: str = ""
        self.queue_name: list = []
        self.rabbit_user: str = ""
        self.rabbit_pass: str = ""
        self.rabbit_connect_string: str = ""

        # Project details
        self.name: str = ""
        self.version: str = ""
        self.description: str = ""
        self.terms: str = ""
        self.contacts: dict = {}
        self.license: dict = {}

        # JWT params
        self.algorithm: str = ""
        self.secret_key: str = ""
        self.token_url: str = ""
        self.grant_type: str = ""
        self.token_expire_min: int = 0
        self.refresh_token_expire_minutes: int = 0

        # Google AUTH
        self.google_client_id: str = ""

        # MSOFT AUTH
        self.msal_login_authority: str = ""
        self.msal_client_id: str = ""
        self.msal_issuer: str = ""

        # News
        self.news_api_key: str = ""
        # admin
        self.email: str = ""
        self.password: str = ""
        self.username: str = ""
        self.is_admin: bool = True
        self.telephone: str = ""
        self.mail_username: str = ""
        self.mail_password: str = ""
        self.mail_port: int = 0
        self.mail_server: str = ""
        self.mail_from_name: str = ""
        self.mail_starttls: bool = False
        self.mail_ssl_tls: bool = False
        self.use_credentials: bool = False
        self.validate_certs: bool = False
        self.email_config: Any = None
        self.security_salt: str = ""

        # client
        self.client_url: str = ""

    def from_toml_file(self):
        self.sql_username = cf.database.user
        self.sql_password = cf.database.pwd
        self.sql_host = cf.database.host
        self.sql_port = cf.database.port
        self.sql_db = cf.database.db
        self.db_url = f"mariadb+aiomysql://{self.sql_username}:{self.sql_password}@{self.sql_host}:{self.sql_port}/{self.sql_db}?charset=utf8mb4"

        self.rabbit_host_name = cf.queue.params.host_name
        self.rabbit_host_port = cf.queue.params.port
        self.rabbit_user = cf.queue.params.user
        self.rabbit_pass = cf.queue.params.pwd
        self.queue_name = cf.queue.params.my_queue
        self.rabbit_connect_string = (
            f"amqp://{self.rabbit_user}:{self.rabbit_pass}@"
            + self.rabbit_host_name
            + ":"
            + self.rabbit_host_port
            + "/"
        )
        self.log_type = cf.api.log_type
        self.host_url = cf.api.host_url
        self.debug = cf.api.debug
        self.auth_type = cf.api.auth_type

        self.pwd_len = cf.hash.password.length
        self.rounds = cf.hash.password.rounds
        self.encoding = cf.hash.password.encoding

        self.name = cf.elyte.api.app["name"]
        self.terms = cf.elyte.api.app.terms_of_service
        self.version = cf.tool.poetry.version
        self.description = cf.elyte.api.app.description
        self.contacts = cf.elyte.contact.as_dict()
        self.license = cf.elyte.contact.license.as_dict()

        self.algorithm = cf.token.params.algorithm
        # self.secret_key = secrets.token_urlsafe(32)
        self.secret_key = cf.token.params.secret_key
        self.token_expire_min = cf.token.params.token_expire_min
        self.refresh_token_expire_minutes = cf.token.params.refresh_token_expire_minutes
        self.grant_type = cf.token.params.grant_type
        self.news_api_key = cf.api.news_api_key

        self.email = cf.admin.email
        self.password = cf.admin.password
        self.username = cf.admin.username
        self.telephone = cf.admin.telephone

        self.mail_username = cf.admin.mail_username
        self.mail_port = cf.admin.mail_port
        self.mail_server = cf.admin.mail_server
        self.mail_from_name = cf.admin.mail_from_name
        self.mail_starttls = cf.admin.mail_starttls
        self.mail_ssl_tls = cf.admin.mail_ssl_tls
        self.use_credentials = cf.admin.use_credentials
        self.validate_certs = cf.admin.validate_certs

        ##Visa Payment API
        self.visa_userid = cf.VDP.userId
        self.visa_password = cf.VDP.password
        self.visa_cert = cf.VDP.cert
        self.visa_key = cf.VDP.key
        self.visa_url = cf.VDP.visaUrl
        self.visa_shared_secret = cf.VDP.sharedSecret

        return self

    def from_env_file(self):
        print("Enviromental variables injected!")

        self.sql_host = str(getenv("MYSQL_HOST"))
        self.sql_db = str(getenv("MYSQL_DATABASE"))
        self.sql_username = str(getenv("MYSQL_USER"))
        self.sql_password = str(getenv("MYSQL_PASSWORD"))
        self.sql_port = int(getenv("MYSQL_PORT"))
        self.host_url = str(getenv("HOST_URL"))
        self.db_url = f"mariadb+aiomysql://{self.sql_username}:{self.sql_password}@{self.sql_host}:{self.sql_port}/{self.sql_db}?charset=utf8mb4"

        self.rabbit_host_name = str(getenv("RABBIT_HOST"))
        self.rabbit_host_port = str(getenv("RABBITMQ_NODE_PORT"))
        self.rabbit_user = str(getenv("RABBITMQ_DEFAULT_USER"))
        self.rabbit_pass = str(getenv("RABBITMQ_DEFAULT_PASS"))
        self.rabbit_connect_string = (
            f"amqp://{self.rabbit_user}:{self.rabbit_pass}@"
            + self.rabbit_host_name
            + ":"
            + self.rabbit_host_port
            + "/%2F"
        )
        self.google_client_id = str(getenv("GOOGLE_CLIENT_ID"))
        self.msal_login_authority = str(getenv("MSAL_LOGIN_AUTHORITY"))
        self.msal_client_id = str(getenv("MSAL_CLIENT_ID"))
        self.msal_issuer = str(getenv("MSAL_ISSUER"))

        self.client_url = str(getenv("CLIENT_URL"))
        self.refresh_token_expire_minutes = int(getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
        self.token_expire_min = int(getenv("TOKEN_EXPIRE_MINUTES"))

        self.security_salt = str(getenv("SECURITY_PASSWORD_SALT"))
        self.mail_password = str(getenv("MAIL_PASSWORD"))
        self.origins = json.loads(getenv("BACKEND_CORS_ORIGINS"))
        self.email_config = ConnectionConfig(
            MAIL_USERNAME=self.mail_username,
            MAIL_PASSWORD=self.mail_password,
            MAIL_FROM=self.email,
            MAIL_PORT=self.mail_port,
            MAIL_SERVER=self.mail_server,
            MAIL_STARTTLS=self.mail_starttls,
            MAIL_SSL_TLS=self.mail_ssl_tls,
            TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
        )
        # TODO
        #self.queue_name = json.loads(getenv("RABBIT_QNAME"))
        # self.email = str(getenv("MAIL_FROM"))
        # self.mail_username = str(getenv("MAIL_USERNAME"))
        # self.mail_port = int(getenv("MAIL_PORT"))
        # self.mail_server = str(getenv("MAIL_SERVER"))
        # self.mail_from_name = str(getenv("MAIL_FROM_NAME"))
        # self.mail_starttls = getenv("MAIL_STARTTLS", "False").lower() == "true"
        # self.mail_ssl_tls = getenv("MAIL_SSL_TLS", "False").lower() == "true"
        # self.use_credentials = getenv("USE_CREDENTIALS", "False").lower() == "true"
        # self.validate_certs = getenv("VALIDATE_CERTS", "False").lower() == "true"
        return self
