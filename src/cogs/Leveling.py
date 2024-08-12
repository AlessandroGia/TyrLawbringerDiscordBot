import io

from discord import Object, Interaction, app_commands, ext, Message, Member, File
from src.leveling.Exping import Exping
from discord.ext import commands

import discord

from src.leveling.Images import Images


class Leveling(ext.commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot: commands.Bot = bot
        self.__exping: Exping = Exping()
        self.__images = Images()

    @staticmethod
    def __is_owner(interaction: Interaction) -> bool:
        return interaction.user.id == interaction.guild.owner.id

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.author.bot:
            await self.__exping.exp(message)

    async def __send_mess(self, interaction: Interaction) -> None:
        current_role, next_role, points_to_lvl = self.__exping.get_roles_and_points_to_lvl(interaction)
        if current_role:
            img = self.__images.create_image(
                current_role,
                interaction.user.name
            )
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                desc = interaction.user.mention
                if next_role:
                    desc += f'***{points_to_lvl}pt.*** left to rank up to **{next_role.name}**.'
                await interaction.response.send_message(
                    desc,
                    file=File(image_binary, 'level.png')
                )
        else:
            await interaction.response.send_message(
                'You have no roles.'
            )



    @app_commands.command(
        name='points',
        description='Get user points.'
    )
    async def points(self, interaction: Interaction) -> None:
        await self.__exping.get_user_points(
            interaction.guild_id,
            interaction.user.id
        )
        self.__send_mess(interaction)

    @app_commands.command(
        name='set-points',
        description='Set user points.'
    )
    @app_commands.describe(
        id='User id',
        points='Number of points'
    )
    @app_commands.check(__is_owner)
    async def set_points(self, interaction: Interaction, id: str, points: int) -> None:
        await self.__exping.set_user_points(
            interaction.guild.id,
            interaction.user,
            points
        )

    @set_points.error
    async def points_error(self, interaction: Interaction, error):
        await interaction.response.send_message(
            "That's no funny!",
            ephemeral=True
        )


async def setup(bot: ext.commands.Bot) -> None:
    await bot.add_cog(
        Leveling(bot),
        guilds=[
            Object(id=928785387239915540)
        ]
    )
