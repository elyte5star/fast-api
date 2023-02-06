from resources.utils.base_functions import Utilities
from resources.database.models.product import Products
from resources.database.models.user import Users
import json
from os import getcwd, listdir
from resources.lib.config import Settings
import asyncio
import logging

pwd = getcwd()
data_path = pwd + "/demo_data/data"
dirs = listdir(data_path)


class SQLTableBuilder(Utilities):
    def __init__(self, cf):
        super().__init__(cf)
        self.session = self._session

    async def read_json(self, filename: str) -> dict:
        try:
            with open(filename, "r") as file_object:
                data = file_object.read()
                return json.loads(data)
        except IOError as e:
            logging.error("Reading file  %s failed due to: %s", filename, e)
            return {}

    async def build_tables_from_json(self):
        for file in dirs:
            path_to_file = f"{data_path}/{file}"
            json_obj = await self.read_json(path_to_file)
            for i, item in enumerate(json_obj):
                print(item)
            break


async def main():
    cfg = Settings().from_toml_file()
    sql_obj = SQLTableBuilder(cfg)
    await sql_obj.build_tables_from_json()


if __name__ == "__main__":
    asyncio.run(main())
    raise SystemExit
