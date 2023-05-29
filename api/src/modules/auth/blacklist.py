from modules.database.models.blacklist import _BlackList
from modules.utils.base_functions import Utilities
from sqlalchemy.sql.expression import false
from typing import Optional


class BlackListHandler(Utilities):
    async def create_blacklist(self, data: dict) -> bool:
        token_info = _BlackList(**data)
        async with self.get_session() as session:
            session.add(token_info)
            await session.commit()
            self.log.info("Blacklist created!")
            return True

    async def blacklist_token(self, token_id: str) -> bool:
        if await self.tokenid_exist(token_id) is not None:
            async with self.get_session() as session:
                await session.execute(
                    self.update(_BlackList)
                    .where(_BlackList.token_id == token_id)
                    .values(dict(active=False))
                    .execution_options(synchronize_session="fetch")
                )
                await session.commit()
                self.log.warning("Token blacklisted!!")
                return True
        self.log.warning("Couldnt Blacklist token,token not found in db!")
        return False

    async def tokenid_exist(self, token_id: str) -> Optional[_BlackList]:
        async with self.get_session() as session:
            result = await session.execute(
                self.select(_BlackList.token_id).where(_BlackList.token_id == token_id)
            )
            return result.first()

    async def is_token_blacklisted(self, token_id: str) -> bool:
        if await self.tokenid_exist(token_id) is not None:
            async with self.get_session() as session:
                result = await session.execute(
                    self.select(_BlackList).where(_BlackList.token_id == token_id)
                )
                (data,) = result.first()
                if data.active == false():
                    return True
        # black list a strange token
        self.log.warning("Token not found in blacklist!")
        return False
