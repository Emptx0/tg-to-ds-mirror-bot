import os
import sys
from typing import Final

from discord import Intents, Client
from dotenv import load_dotenv

load_dotenv()
TOKEN_DS: Final[str] = os.getenv('TOKEN_DS')
CHANNEL_ID: Final[int] = int(os.getenv('DS_CHANNEL'))

intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

message = sys.argv[1]


@client.event
async def on_ready() -> None:
    await client.get_channel(CHANNEL_ID).send(message)
    quit()


if __name__ == '__main__':
    client.run(TOKEN_DS)
