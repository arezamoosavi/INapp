from os import getenv
import asyncpg
from datetime import datetime

from tortoise import Tortoise
from db.models import userstatus

"""
URL= postgresql-svc.default.svc.cluster.local:5432
POSTGRES_URL=postgresql://user:password@postgresql-svc.default.svc.cluster.local:5432/testdb
"""


class TorPostgre:
    def __init__(self):
        self.db_url = getenv(
            "POSTGRES_URL",
            "postgres://user:password@postgresql-svc.default.svc.cluster.local:5432/testdb",
        )

    async def initdb(self):
        await Tortoise.init(db_url=self.db_url, modules={"models": ["db.models"]})
        await Tortoise.generate_schemas()

    async def checkall(self):
        await self.initdb()
        print(await userstatus.all())


class Postgres:
    def __init__(self):
        self.db_url = getenv(
            "POSTGRES_URL",
            "postgres://user:password@postgresql-svc.default.svc.cluster.local:5432/testdb",
        )

    async def checkConnection(self):
        conn = await asyncpg.connect(self.db_url)
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS testusers(
                id serial PRIMARY KEY,
                name text,
                dob date
                    )
                """
        )

        # Insert a record into the created table.
        await conn.execute(
            """
            INSERT INTO testusers(name, dob) VALUES($1, $2)
            """,
            "Bob",
            datetime.utcnow(),
        )

        # Select a row from the table.
        row = await conn.fetchrow("SELECT * FROM testusers WHERE name = $1", "Bob")

        print(dict(row), type(row))

        # test ideas:1
        print("------test idea1---------")
        record = ("Ali", datetime.utcnow())
        await conn.execute(
            """
            INSERT INTO testusers(name, dob) VALUES($1, $2)
            """,
            record[0],
            record[1],
        )
        allrow = await conn.fetch("SELECT name FROM testusers")
        print(allrow, type(allrow))

        print([dict(row) for row in allrow])
        print("# test ideas:1 :::::SAVED to USD_BTC table!!")

        # test ideas:2
        print("------test idea2---------")
        db = "testusers"
        trow = await conn.fetch("SELECT name FROM {}".format(db))
        print(trow[-1])
        print("# test ideas:2 :::::Got it!!")

        # test ideas:3
        print("------test idea3---------")
        record = ("Alireza", datetime.utcnow())
        que = """INSERT INTO {}(name, dob) VALUES($1, $2)""".format("testusers")
        await conn.execute(que, record[0], record[1])

        allrow = await conn.fetch("SELECT name FROM {}".format("testusers"))
        print(allrow, type(allrow))
        print([dict(row) for row in allrow])
        print("# test ideas:3 :::::Worked!!")

        # Drop Table
        query = "DROP TABLE IF EXISTS {} CASCADE;".format("testusers")
        await conn.execute(query)

        print("\n\n", "connection was succesfull!", "\n\n", datetime.utcnow(), "\n\n\n")
        await conn.close()
