import discord

from discord import Object, Interaction, app_commands, ext, Message, Member, InteractionResponse
from random import randint as r
from discord.ext import commands

from src.StatsXp.StatsXp import StatsXp


class Law(ext.commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.__bot: commands.Bot = bot
        self.__idle: discord.Status = discord.Status.idle
        self.__offline: discord.Status = discord.Status.offline
        self.__stats: StatsXp = StatsXp()
        self.__quotes_on_leave: list = [
            "No, that's no.", "That\'s no funny.", "Idiocy is not a defense.", "You cannot stop justice!",
            "Begone foul creature!", "The wicked fall before me!",
        ]
        self.__quotes_on_join: list = [
            "HAI!"
        ]
        self.__quotes_on_ban: list = [
            "We don't have time for jokes!", "You chose this, remember that.",
            "I take no joy in what must be done!"
        ]

    @staticmethod
    def __is_owner(interaction: Interaction):
        return interaction.user.id == interaction.guild.owner.id

    @app_commands.command(
        name='setpoints',
        description='Set user points.'
    )
    @app_commands.describe(
        id='User id',
        points='Number of points'
    )
    async def setpoints(self, interaction: Interaction, id: str, points: int):
        if self.__is_owner(interaction):
            await self.__stats.set_user_points(interaction, int(id), points)

    @app_commands.command(
        name='points',
        description='Get user points.'
    )
    async def points(self, interaction: Interaction):
        await self.__stats.get_user_points(interaction)

    async def __set_afk(self, message: Message):
        author_id: int = message.author.id
        owner: Member = message.guild.get_member(message.guild.owner_id)
        if self.__bot.application_id != author_id and owner.id != author_id and (owner.status == self.__idle or owner.status == self.__offline):
            await message.channel.send(self.__quotes_on_leave[r(0, len(self.__quotes_on_leave) - 1)])

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        await self.__set_afk(message)
        await self.__stats.exp(message)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        role = discord.utils.get(member.guild.roles, name='Yokai')
        channel = member.guild.get_channel(1098908138570256464)
        await member.add_roles(role)
        await channel.send(f'{member.mention} {self.__quotes_on_join[r(0, len(self.__quotes_on_join) - 1)]}')

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = member.guild.get_channel(1098908138570256464)
        await channel.send(f'{member.name} {self.__quotes_on_leave[r(0, len(self.__quotes_on_leave) - 1)]}')

    @commands.Cog.listener()
    async def on_member_ban(self, member: Member):
        channel = member.guild.get_channel(1098908138570256464)
        await channel.send(f'{member.name} {self.__quotes_on_ban[r(0, len(self.__quotes_on_ban) - 1)]}')


async def setup(bot: ext.commands.Bot):
    await bot.add_cog(Law(bot), guilds=[Object(id=928785387239915540)])
