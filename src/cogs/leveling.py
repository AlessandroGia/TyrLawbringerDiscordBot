import io

import discord
from discord import Interaction, app_commands, ext, Message, File
from discord.app_commands import Transform

from src.converters.user_converter import GuildUsers
from src.modules.leveling.exping import Exping
from discord.ext import commands

from src.modules.leveling.images import Images
from PIL import Image


class Leveling(ext.commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot: commands.Bot = bot
        self.__exping: Exping = Exping(bot)
        self.__images: Images = Images()

    async def __send_mess(self, interaction: Interaction) -> None:
        current_role, next_role, points_to_lvl = self.__exping.get_roles_and_points_to_lvl(interaction)
        desc = interaction.user.mention

        if next_role:
            desc += f' ***{points_to_lvl}pt.*** left to rank up to **{next_role.name}**.'
        if current_role:
            img: Image = self.__images.create_image(
                current_role,
                interaction.user.display_name
            )
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                file = File(image_binary, 'level.png')
                await interaction.response.send_message(desc, file=file)
        else:
            await interaction.response.send_message(content=desc)

    @app_commands.command(
        name='points',
        description='Get user points.'
    )
    async def points(self, interaction: Interaction) -> None:
        await self.__exping.get_user_points(
            interaction.guild_id,
            interaction.user.id
        )
        await self.__send_mess(interaction)

    @app_commands.command(
        name='set-points',
        description='Set user points.'
    )
    @app_commands.describe(
        user='Username',
        points='Number of points'
    )
    @commands.is_owner()
    async def set_points(self, interaction: Interaction, user: Transform[discord.Member, GuildUsers], points: app_commands.Range[int, 0]) -> None:
        await self.__exping.set_user_points(
            interaction.guild_id,
            user,
            points
        )
        await interaction.response.send_message(
            f'{user.display_name} has been set to {points} points.'
        )

    @set_points.error
    async def points_error(self, interaction: Interaction, error):
        if isinstance(error, commands.errors.CheckFailure):
            await interaction.response.send_message(
                "That's no funny!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Error",
                ephemeral=True
            )


    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.author.bot:
            await self.__exping.exp(message)

async def setup(bot: ext.commands.Bot) -> None:
    await bot.add_cog(Leveling(bot))
