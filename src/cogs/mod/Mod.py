from discord import Object, Interaction, app_commands, ext, Message, Member
from src.StatsXp.StatsXp import StatsXp
from discord.ext import commands
from random import randint as r


import discord


class Law(ext.commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.__bot: commands.Bot = bot
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

    def __id_bot(self, interaction: Interaction):
        return interaction.user.id == self.__bot.application_id

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
        owner: Member = message.guild.owner
        if self.__bot.application_id != author_id and owner.id != author_id and (
                owner.status == discord.Status.idle or owner.status == discord.Status.offline or owner.status == discord.Status.dnd
        ) and owner in message.mentions:
            await message.channel.send(self.__quotes_on_leave[r(0, len(self.__quotes_on_leave) - 1)])

    async def __ping_bot(self, message: Message):
        if self.__bot.application.id in [mem.id for mem in message.mentions] and not self.__bot.application_id == message.author.id:
            if message.author.id == message.guild.owner_id:
                await message.channel.send(f'{message.author.mention} HAI!')
            else:
                await message.channel.send(f'{message.author.mention} {self.__quotes_on_ban[r(0, len(self.__quotes_on_ban) - 1)]}')

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        await self.__set_afk(message)
        await self.__ping_bot(message)
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
