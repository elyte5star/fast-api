from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from modules.database.base import Base
from fastapi.logger import logger
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from typing import Optional
import uuid
from contextlib import asynccontextmanager

# needed to create table automatically

from .models.user import _User
from .models.booking import _Booking
from .models.blacklist import _BlackList
from .models.job_task import _Job, _Task
from .models.worker import _Worker
from .models.product import Product, SpecialDeals
from sqlalchemy import or_
from sqlalchemy.orm import selectinload, defer


class AsyncDatabaseSession:
    def __init__(self, cf):
        self._engine = None
        self._session = None
        self.select = select
        self.update = update
        self.delete = delete
        self.log = logger
        self.cf = cf

    def async_session_generator(self) -> AsyncSession:
        try:
            self._engine = create_async_engine(
                self.cf.db_url,
                future=True,
                echo=False,
            )
            self._session = sessionmaker(
                self._engine, expire_on_commit=False, class_=AsyncSession
            )()
            self.log.info("[+] MYSQL/MARIADB Connection created successfully.")
            return self._session
        except Exception as ex:
            self.log.warning(
                "Connection could not be made due to the following error: \n",
                ex,
            )

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        try:
            async with self.async_session_generator() as session:
                yield session
        except IntegrityError as e:
            await session.rollback()
            self.log.warning(e)
        finally:
            self.log.warning("[+] Closing connection to MYSQL/MARIA database!")
            await session.close()

    async def create_all(self):
        async with self._engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await self.create_admin_account()

    async def username_email_exists(self, email: str, username: str) -> Optional[_User]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_User.email, _User.username).where(
                    or_(_User.email == email, _User.username == username)
                )
            )
            return result.first()

    async def userid_exist(self, userid: str) -> Optional[_User]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_User.userid).where(_User.userid == userid)
            )
            return result.first()

    async def username_exist(self, username: str) -> Optional[_User]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_User.username).where(_User.username == username)
            )
            return result.first()

    async def pid_exist(self, pid: str) -> Optional[Product]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(Product.pid).where(Product.pid == pid)
            )
            return result.first()

    async def product_name_exist(self, name: str) -> Optional[Product]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(Product.name).where(Product.name == name)
            )
            return result.first()

    async def oid_exist(self, oid: str) -> Optional[_Booking]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_Booking.oid).where(_Booking.oid == oid)
            )
            return result.first()

    async def job_exist(self, job_id: str) -> Optional[_Job]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_Job.job_id).where(_Job.job_id == job_id)
            )
            return result.first()

    async def create_admin_account(self):
        if await self.username_email_exists(self.cf.email, self.cf.username) is None:
            admin_user = _User(
                userid=str(uuid.uuid4()),
                email=self.cf.email,
                password=self.cf.password,
                username=self.cf.username,
                telephone=self.cf.telephone,
                admin=self.cf.is_admin,
            )
            async with self.get_session() as session:
                async with session.begin():
                    session.add(admin_user)
                    self.log.info("Tables created successfully!!")
                    self.log.info("Admin account created successfully!!")
        else:
            self.log.info("Admin account exist already!!")
