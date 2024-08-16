from discord import Object, Interaction, app_commands, ext, Message, Member
from discord.ext import commands

import discord

from src.quotes.Quotes import Quotes


class Law(ext.commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot: commands.Bot = bot
        self.__quotes: Quotes = Quotes()

        self.__welcome_channel: int = 1098908138570256464
        self.__id_bot_role: int = 1006641555421016227
        self.__role_join: int = 928793792994213908

    async def __set_afk(self, message: Message) -> None:
        owner: Member = message.guild.owner
        if owner.id != message.author.id and (
                owner.status == discord.Status.idle or owner.status == discord.Status.offline or owner.status == discord.Status.dnd
        ) and owner in message.mentions:
            await message.reply(
                content=self.__quotes.get_random(self.__quotes.quotes_on_leave),
                mention_author=True
            )

    async def __ping_bot(self, message: Message) -> None:
        id_mentions = [mes.id for mes in message.mentions]
        id_role_mentions = [role.id for role in message.role_mentions]
        if self.__bot.application_id in id_mentions or self.__id_bot_role in id_role_mentions:
            if message.author.id == message.guild.owner_id:
                await message.reply(
                    content=f'HAI!',
                    mention_author=True
                )
            else:
                await message.reply(
                    content=self.__quotes.get_random(self.__quotes.quotes_on_ping),
                    mention_author=True
                )

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message and not message.author.bot:
            await self.__set_afk(message)
            await self.__ping_bot(message)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        role = member.guild.get_role(self.__role_join)
        channel = member.guild.get_channel(self.__welcome_channel)
        await member.add_roles(role)
        await channel.send(
            content=self.__quotes.get_random(self.__quotes.quotes_on_join),
            mention_author=True
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        channel = member.guild.get_channel(self.__welcome_channel)
        await channel.send(
            content=self.__quotes.get_random(self.__quotes.quotes_on_leave),
            mention_author=True
        )

    @commands.Cog.listener()
    async def on_member_ban(self, member: Member) -> None:
        channel = member.guild.get_channel(self.__welcome_channel)
        await channel.send(
            content=self.__quotes.get_random(self.__quotes.quotes_on_ban),
            mention_author=True
        )


async def setup(bot: ext.commands.Bot) -> None:
    await bot.add_cog(Law(bot), guilds=[Object(id=928785387239915540)])
