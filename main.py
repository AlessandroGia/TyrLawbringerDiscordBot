from discord import Intents, Object, Status, Activity, ActivityType
from discord.ext import commands
from dotenv import load_dotenv

import os


class TyrLawbringer(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=Intents.all(),
            activity=Activity(type=ActivityType.competing, name="Law")
        )

    async def setup_hook(self) -> None:
        await self.load_extension(f"src.cogs.mod.Mod")

    async def on_ready(self) -> None:
        await self.tree.sync(guild=Object(id=928785387239915540))
        print("{} si e' connesso a discord!".format(self.user))


if __name__ == "__main__":
    load_dotenv()
    TyrLawbringer().run(os.getenv("DISCORD_TOKEN"))
