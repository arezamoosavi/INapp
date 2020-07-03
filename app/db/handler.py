from os import getenv
import asyncpg
from datetime import datetime


class pgQuery:
    def __init__(self):
        self.db_url = getenv(
            "POSTGRES_URL",
            "postgres://user:password@postgresql-svc.default.svc.cluster.local:5432/testdb",
        )

    async def saveData(self, database, username, password):

        conn = await asyncpg.connect(self.db_url)
        query = """INSERT INTO {}(username, password, created_at) 
                    VALUES($1, $2, $3)""".format(
            database
        )

        await conn.execute(query, username, password, datetime.now().isoformat())
        await conn.close()
        return "\nSAVED\n"

    async def getAll(self, database):

        conn = await asyncpg.connect(self.db_url)
        rows = await conn.fetch("SELECT * FROM {}".format(database))
        await conn.close()
        return [dict(row) for row in rows]

