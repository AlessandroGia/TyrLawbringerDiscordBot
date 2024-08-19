import io

from discord import Object, Interaction, app_commands, ext, Message, File
from src.leveling.Exping import Exping
from discord.ext import commands


from src.leveling.Images import Images
from PIL import Image


class Leveling(ext.commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot: commands.Bot = bot
        self.__exping: Exping = Exping(bot)
        self.__images: Images = Images()

    @staticmethod
    def __is_owner(interaction: Interaction) -> bool:
        return interaction.user.id == interaction.guild.owner.id

    async def __send_mess(self, interaction: Interaction) -> None:
        current_role, next_role, points_to_lvl = self.__exping.get_roles_and_points_to_lvl(interaction)
        if current_role:
            img: Image = self.__images.create_image(
                current_role,
                interaction.user.name
            )
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                desc = interaction.user.mention
                if next_role:
                    desc += f' ***{points_to_lvl}pt.*** left to rank up to **{next_role.name}**.'
                await interaction.response.send_message(
                    desc,
                    file=File(image_binary, 'level.png')
                )
        else:
            await interaction.response.send_message(
                content=interaction.user.mention + f' ***{points_to_lvl}pt.*** left to rank up to **{next_role.name}**.'
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
        await self.__send_mess(interaction)

    @app_commands.command(
        name='set-points',
        description='Set user points.'
    )
    @app_commands.describe(
        user_id='User id',
        points='Number of points'
    )
    @app_commands.check(__is_owner)
    async def set_points(self, interaction: Interaction, user_id: str, points: int) -> None:
        await self.__exping.set_user_points(
            interaction.guild_id,
            interaction.guild.get_member(int(user_id)),
            points
        )
        await interaction.response.send_message(
            f'{self.__bot.get_user(int(user_id)).name} has been set to {points} points.'
        )

    @set_points.error
    async def points_error(self, interaction: Interaction, error):
        await interaction.response.send_message(
            "That's no funny!",
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.author.bot:
            await self.__exping.exp(message)


async def setup(bot: ext.commands.Bot) -> None:
    await bot.add_cog(
        Leveling(bot),
        guilds=[
            Object(id=928785387239915540)
        ]
    )
