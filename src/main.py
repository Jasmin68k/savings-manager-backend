"""The start module of the savings manager app."""
import asyncio
from pprint import pprint

from src.singleton import db_manager

async def main():
    moneybox_data = {
        "nam": "Notgroschen 4",
    }

    new_moneybox = await db_manager.add_moneybox(moneybox_data=moneybox_data)
    pprint(new_moneybox)


if __name__ == "__main__":
    asyncio.run(main())
