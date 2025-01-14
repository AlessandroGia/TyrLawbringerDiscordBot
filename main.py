from discord import Intents, Object, Status, Activity, ActivityType, VoiceProtocol
from discord.ext import commands
from dotenv import load_dotenv

from config import Config
import os


class TyrLawbringer(commands.Bot):
    def __init__(self) -> None:
        self.__config: Config = Config()
        self.vc: VoiceProtocol | None = None
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=Intents.all(),
            activity=Activity(
                type=ActivityType.competing,
                name="Law"
            )
        )

    async def setup_hook(self) -> None:
        await self.load_cogs()

    async def on_ready(self) -> None:
        await self.tree.sync()
        self.vc: VoiceProtocol = await self.get_channel(int(self.__config.get('channels.private'))).connect()
        print("{} si e' connesso a discord!".format(self.user))

    async def load_cogs(self) -> None:
        root: str = os.path.dirname(os.path.abspath(__file__))
        files: list[str] = os.listdir(os.path.join(root, 'src', 'cogs'))
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                try:
                    await self.load_extension(f'src.cogs.{file[:-3]}')
                    print(file[:-3], 'Loaded')
                except Exception as e:
                    print(file[:-3], f'Not loaded: {e}')


if __name__ == "__main__":
    load_dotenv()
    TyrLawbringer().run(os.getenv("DISCORD_TOKEN"))
