from resources.database.models.blacklist import BlackList
from resources.utils.base_functions import Utilities
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import false


class BlackListHandler(Utilities):
    async def create_blacklist(self, payload: BlackList) -> bool:
        self.add(payload)
        try:
            await self.commit()
            self.log.info("Blacklist created!")
            return True
        except IntegrityError as e:
            await self.rollback()
            self.log.warning(f"Blacklist creation failed!{e}")
            return False

    async def blacklist_token(self, token_id: str) -> bool:
        if token_id:
            query = (
                self.update(BlackList)
                .where(BlackList.token_id == token_id)
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

        return False

    async def is_token_blacklisted(self, token_id: str) -> bool:
        print(token_id)
        query = self.select(BlackList).where(BlackList.token_id == token_id)
        tokens = await self.execute(query)
        if tokens is not None:
            (token,) = tokens.first()
            if token.active == false():
                return True
        # black list a strange token
        return False
