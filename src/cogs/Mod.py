from discord import Object, Interaction, app_commands, ext, Message, Member
from src.leveling.Leveling import Leveling
from discord.ext import commands

import discord

from src.quotes.Quotes import Quotes


class Law(ext.commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot: commands.Bot = bot
        self.__leveling: Leveling = Leveling()
        self.__quotes: Quotes = Quotes()
        self.__leveling: Leveling = Leveling()

        self.__channel_bot: int = 1098908138570256464
        self.__role_join: str = 'Yokai'

    @staticmethod
    async def __not_permitted(interaction: Interaction):
        await interaction.response.send_message("That's no funny!", ephemeral=True)

    @staticmethod
    def __is_owner(interaction: Interaction) -> bool:
        return interaction.user.id == interaction.guild.owner.id

    def __id_bot(self, interaction: Interaction) -> bool:
        return interaction.user.id == self.__bot.application_id

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
        await self.__leveling.set_user_points(interaction, int(id), points)

    @set_points.error
    async def points_error(self, interaction: Interaction, error):
        self.__not_permitted(interaction)

    @app_commands.command(
        name='points',
        description='Get user points.'
    )
    async def points(self, interaction: Interaction) -> None:
        await self.__leveling.get_user_points(interaction)

    async def __set_afk(self, message: Message) -> None:
        author_id: int = message.author.id
        owner: Member = message.guild.owner
        if self.__bot.application_id != author_id and owner.id != author_id and (
                owner.status == discord.Status.idle or owner.status == discord.Status.offline or owner.status == discord.Status.dnd
        ) and owner in message.mentions:
            await message.channel.send(
                f'{message.author.mention} {self.__quotes.get_random(self.__quotes.quotes_on_leave)}'
            )

    async def __ping_bot(self, message: Message) -> None:
        if self.__bot.application.id in [mem.id for mem in message.mentions] and not self.__bot.application_id == message.author.id:
            if message.author.id == message.guild.owner_id:
                await message.channel.send(f'{message.author.mention} HAI!')
            else:
                await message.channel.send(
                    f'{message.author.mention} {self.__quotes.get_random(self.__quotes.quotes_on_ban)}'
                )

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message:
            await self.__set_afk(message)
            await self.__ping_bot(message)
            #await self.__leveling.exp(message, self.__bot.application_id)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        role = discord.utils.get(member.guild.roles, name=self.__role_join)
        channel = member.guild.get_channel(self.__channel_bot)
        await member.add_roles(role)
        await channel.send(f'{member.mention} {self.__quotes.get_random(self.__quotes.quotes_on_join)}')

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        channel = member.guild.get_channel(self.__channel_bot)
        await channel.send(f'{member.name} {self.__quotes.get_random(self.__quotes.quotes_on_leave)}')

    @commands.Cog.listener()
    async def on_member_ban(self, member: Member) -> None:
        channel = member.guild.get_channel(self.__channel_bot)
        await channel.send(f'{member.name} {self.__quotes.get_random(self.__quotes.quotes_on_ban)}')


async def setup(bot: ext.commands.Bot) -> None:
    await bot.add_cog(Law(bot), guilds=[Object(id=928785387239915540)])
