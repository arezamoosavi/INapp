import logging
import asyncio
from db.connection import Postgres, TorPostgre


logging.basicConfig(
    filename="dblog.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)


async def main():

    conn = Postgres()
    await conn.checkConnection()

    tor_db = TorPostgre()
    await tor_db.checkall()


if __name__ == "__main__":

    try:
        asyncio.get_event_loop().run_until_complete(main())

        exit(1)

    except Exception as e:

        logging.error("Error! {}".format(e))
        exit(0)
