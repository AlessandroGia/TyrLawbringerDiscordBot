import asyncio

import discord

from discord import Object, ext, Message, Member, app_commands, Interaction, VoiceState
from discord.app_commands import Transform

from src.custom_transformers.custom_transformers import ChannelUsers
from src.quotes.quotes import Quotes
from config import waiting_typing, Config
from discord.ext import commands
from enum import Enum


class Actions(Enum):
    JOIN = 1
    LEAVE = 2
    BAN = 3


class Law(ext.commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot: commands.Bot = bot
        self.__quotes: Quotes = Quotes()

        config = Config()

        self.__welcome_channel: int = int(config.get('channels.welcome'))
        self.__id_tyr_role: int = int(config.get('roles.tyr'))
        self.__role_join: int = int(config.get('roles.join'))

    @app_commands.command(
        name='ping',
        description='Fa pingare l\'utente.'
    )
    async def ping(self, interaction: Interaction, user: Transform[discord.Member, ChannelUsers]) -> None:
        await interaction.response.send_message(
            user.mention,
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message and not message.author.bot:
            await self.__set_afk(message)
            await self.__ping_bot(message)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        role: discord.Role = member.guild.get_role(self.__role_join)
        channel: discord.TextChannel = member.guild.get_channel(self.__welcome_channel)

        await member.add_roles(role)
        await self.__send_from_event(Actions.JOIN, channel)

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        channel: discord.TextChannel = member.guild.get_channel(self.__welcome_channel)

        await self.__send_from_event(Actions.LEAVE, channel)

    @commands.Cog.listener()
    async def on_member_ban(self, member: Member) -> None:
        channel: discord.TextChannel = member.guild.get_channel(self.__welcome_channel)

        await self.__send_from_event(Actions.BAN, channel)


    async def __set_afk(self, message: Message) -> None:
        owner: Member = message.guild.owner

        if (
            owner.id != message.author.id
            and owner.status in {discord.Status.idle, discord.Status.offline, discord.Status.dnd}
            and owner in message.mentions
        ):
            content = self.__quotes.get_random(self.__quotes.quotes_on_ban)
            async with message.channel.typing():
                await asyncio.sleep(waiting_typing(content))
            await message.reply(content=content, mention_author=True)

    async def __ping_bot(self, message: Message) -> None:
        if self.__bot.application_id in {m.id for m in message.mentions} or self.__id_tyr_role in {r.id for r in message.role_mentions}:
            content = 'HAI!' if message.author.id == message.guild.owner_id else self.__quotes.get_random(self.__quotes.quotes_on_ping)
            async with message.channel.typing():
                await asyncio.sleep(waiting_typing(content))
            await message.reply(content=content, mention_author=True)

    async def __send_from_event(self, action: Actions, channel: discord.TextChannel) -> None:
        content: str = ''
        if action == Actions.JOIN:
            content = self.__quotes.get_random(self.__quotes.quotes_on_join)
        elif action == Actions.LEAVE:
            content = self.__quotes.get_random(self.__quotes.quotes_on_leave)
        elif action == Actions.BAN:
            content = self.__quotes.get_random(self.__quotes.quotes_on_ban)

        if content:
            async with channel.typing():
                await asyncio.sleep(waiting_typing(content))
            await channel.send(content=content, mention_author=True)

async def setup(bot: ext.commands.Bot) -> None:
    await bot.add_cog(Law(bot))
