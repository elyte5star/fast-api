from modules.database.models.blacklist import _BlackList
from modules.utils.base_functions import Utilities
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import false


class BlackListHandler(Utilities):
    async def create_blacklist(self, data) -> bool:
        token_info = _BlackList(**data.dict())
        self.add(token_info)
        try:
            await self.commit()
            self.log.info("Blacklist created!")
            return True
        except IntegrityError as e:
            await self.rollback()
            self.log.warning(f"Blacklist creation failed!{e}")
            return False
        finally:
            await self._engine.dispose()

    async def blacklist_token(self, token_id: str) -> bool:
        if token_id:
            query = (
                self.update(_BlackList)
                .where(_BlackList.token_id == token_id)
                .values(dict(active=False))
                .execution_options(synchronize_session="fetch")
            )
            await self.execute(query)
            try:
                await self.commit()
                return True
            except IntegrityError as e:
                self.log.info(f"Couldnt Blacklist token!{e}")
                await self.rollback()
                return False
            finally:
                await self._engine.dispose()
        return False

    async def is_token_blacklisted(self, token_id: str) -> bool:
        result = await self.execute(
            self.select(_BlackList).where(_BlackList.token_id == token_id)
        )
        if token_id and result is not None:
            (data,) = result.first()
            if data.active == false():
                return True
        # black list a strange token
        return False
