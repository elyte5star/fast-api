from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from resources.database.base import Base
from fastapi.logger import logger
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from typing import Optional
import uuid

# needed to create table automatically
from .models.product import Product, SpecialDeals
from .models.user import User
from .models.booking import Booking
from .models.blacklist import BlackList
from .models.job_task import _Job, _Task
from .models.worker import _Worker


class AsyncDatabaseSession:
    _session = None  # Ensure db initialized once.

    def __init__(self, cf):
        self._engine = None
        self.select = select
        self.update = update
        self.delete = delete
        self.log = logger
        self.cf = cf
        if AsyncDatabaseSession._session is None:
            self.int_db()

    def int_db(self):
        try:
            self._engine = create_async_engine(
                self.cf.db_url,
                future=True,
                echo=False,
            )
            AsyncDatabaseSession._session = sessionmaker(
                self._engine, expire_on_commit=False, class_=AsyncSession
            )()
            self.log.info(
                f"[+] MYSQL Connection to the {self.cf.sql_host} for user {self.cf.sql_username} created successfully."
            )

        except Exception as ex:
            self.log.warning(
                "Connection could not be made due to the following error: \n",
                ex,
            )

    def __getattr__(self, name) -> AsyncSession:
        return getattr(self._session, name)

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await self.create_admin_account()

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self._engine.begin() as conn:
            result = await conn.execute(
                self.select(User).where(User.email == email)
            )
            return result.first()

    async def create_admin_account(self):
        if await self.get_by_email(self.cf.email) is None:
            admin_user = User(
                userid=str(uuid.uuid4()),
                email=self.cf.email,
                password=self.cf.password,
                username=self.cf.username,
                telephone=self.cf.telephone,
                admin=self.cf.is_admin,
            )
            self.add(admin_user)
            try:
                await self.commit()
                await self.refresh(admin_user)
                self.log.info("Tables created successfully!!")
                self.log.info("Admin account created successfully!!")
            except IntegrityError as e:
                self.log.warning(e)
                await self.rollback()
        else:
            self.log.info("Admin account exist already!!")
