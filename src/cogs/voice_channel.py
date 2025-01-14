import asyncio
import os.path
from asyncio import Event

import discord
from discord import ext, Object, Member, VoiceState, VoiceClient, app_commands, Interaction, VoiceChannel, utils, \
    VoiceProtocol
from discord.app_commands import Transform
from discord.ext import commands

from src.checks.voice_channel_checks import check_voice_channel
from src.custom_transformers.custom_transformers import GuildUsersVip, GuildUsers, Skins
from src.exceptions.voice_channel_exceptions import UserNotConnected, BotNotConnected, BotAlreadyConnected, UserNotInBotVc
from src.exceptions.vgs_exceptions import InexistentVGS, MissingVGS, InexistentSkin

from src.embed.embed import EmbedFactory
from src.voice_state.voice_guild_data import VoiceGuildData
from src.voice_state.voicelines import VoiceLines
from config import Config


class VoiceChannelCog(ext.commands.Cog):


    def __init__(self, bot: ext.commands.Bot):
        self.__bot = bot
        self.__embed = EmbedFactory()

        config = Config()

        self.__private_channel_id: int = int(config.get('channels.private'))
        self.__private_channel: VoiceChannel = self.__bot.get_channel(self.__private_channel_id)
        self.__inactivity_channel: int = int(config.get('channels.inactivity'))

        self.__voice_guild_data: dict[int, VoiceGuildData] = {}
        self.__voice_lines: VoiceLines = VoiceLines()
        

    def __get_voice_guild_data(self, guild_id: int) -> VoiceGuildData:
        if guild_id not in self.__voice_guild_data:
            self.__voice_guild_data[guild_id] = VoiceGuildData()
        return self.__voice_guild_data[guild_id]

    async def __check_user_and_move(self, member: Member) -> None:
        if self.__get_voice_guild_data(member.guild.id).pop_member_in_private(member):
            private_channel = self.__bot.get_channel(self.__private_channel_id)
            if member.voice and member.voice.channel != private_channel:
                await member.move_to(private_channel)

    async def __check_temp_channels(self, member: Member) -> None:
        private_channel = self.__bot.get_channel(self.__private_channel_id)
        channels: list[VoiceChannel] = [
            channel for channel in member.guild.voice_channels
            if channel.id != private_channel.id and channel.id != self.__inactivity_channel
        ]
        guild_data: VoiceGuildData = self.__get_voice_guild_data(member.guild.id)
        empty_channels: list[VoiceChannel] = [channel for channel in channels if not channel.members]

        if not empty_channels and not guild_data.max_channels():
            await guild_data.new_temp_channel(member.guild, channels)
        elif len(empty_channels) > 1 and guild_data.num_temp_channels() > 0:
            await guild_data.remove_temp_channel()

    @ext.commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):

        if not member.bot:
            vc: VoiceClient = self.__bot.vc
            if vc and vc.channel:
                private_channel: VoiceChannel = self.__bot.get_channel(self.__private_channel_id)
                if vc.channel != private_channel and not any(not usr.bot for usr in vc.channel.members):
                    await self.__leave()

        if not before.channel and after.channel:
            await self.__check_user_and_move(member)

        if before.channel != after.channel:
            await self.__check_temp_channels(member)

    @app_commands.command(
        name='add_private',
        description='Fa joinare l\'utente al canale privato.'
    )
    @commands.is_owner()
    async def add_private(self, interaction: Interaction, user: Transform[discord.Member, GuildUsersVip]) -> None:
        private_channel = self.__bot.get_channel(self.__private_channel_id)
        if user.voice and user.voice.channel != private_channel:
            await user.move_to(private_channel)
            await interaction.response.send_message(
                f'{user.display_name} è stato spostato nel canale privato.',
                ephemeral=True
            )
        elif user.voice.channel != private_channel:
            self.__get_voice_guild_data(interaction.guild_id).add_member_to_private(user)
            await interaction.response.send_message(
                f'{user.display_name} è stato aggiunto alla lista del canale privato.',
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f'{user.display_name} è già presente nel canale privato.',
                ephemeral=True
            )

    @app_commands.command(
        name='remove_private',
        description='Rimuove l\'utente dalla lista canale privato.'
    )
    @commands.is_owner()
    async def remove_private(self, interaction: Interaction, user: Transform[discord.Member, GuildUsers]) -> None:
        if self.__get_voice_guild_data(interaction.guild_id).pop_member_in_private(user):
            await interaction.response.send_message(
                f'{user.display_name} è stato rimosso dalla lista del canale privato.',
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f'{user.display_name} non è presente nella lista del canale privato.',
                ephemeral=True
            )

    async def send_error(self, interaction: Interaction, error: str) -> None:
        await interaction.response.send_message(
            embed=self.__embed.error(error),
            ephemeral=True,
            delete_after=5
        )

    async def __send_message(self, interaction: Interaction, message: str) -> None:
        await interaction.response.send_message(
            embed=self.__embed.embed(message, interaction.user),
            ephemeral=True,
            delete_after=3
        )

    @app_commands.command(
        name='join',
        description='Fa joinare il bot al canale vocale.'
    )
    @check_voice_channel()
    async def join(self, interaction: Interaction) -> None:
        if self.__bot.vc:
            await self.__bot.vc.disconnect()
        self.__bot.vc = await interaction.user.voice.channel.connect()
        self.__bot.vc.play(discord.FFmpegPCMAudio(self.__voice_lines.join()))
        await self.__send_message(interaction, f'Bot entrato in **{interaction.user.voice.channel.name}**.')

    async def __leave(self) -> None:
        await self.__bot.vc.disconnect()
        self.__bot.vc = await self.__bot.get_channel(self.__private_channel_id).connect()

    @app_commands.command(
        name='leave',
        description='Fa uscire il bot dal canale vocale.'
    )
    @check_voice_channel()
    async def leave(self, interaction: Interaction) -> None:
        private_channel = self.__bot.get_channel(self.__private_channel_id)
        if self.__bot.vc.channel != private_channel:
            event = Event()
            self.__bot.vc.play(discord.FFmpegPCMAudio(self.__voice_lines.leave()), after=lambda e: asyncio.run_coroutine_threadsafe(self.__leave(), self.__bot.loop))
            await self.__send_message(interaction, 'Bot uscito dal canale vocale.')
        else:
            await self.__send_message(interaction, 'Il bot è già nel canale privato.')

    @app_commands.command(
        name='play',
        description='Fa riprodurre una vgs.'
    )
    @app_commands.describe(
        skin='Skin',
        vgs='Vgs'
    )
    @check_voice_channel()
    async def play(self, interaction: Interaction, skin: Transform[str, Skins], vgs: str) -> None:
        file = self.__voice_lines.get_ogg(skin, vgs)
        await self.__send_message(
            interaction,
            f'***{vgs.replace("_", " ").capitalize()}*** in riproduzione.',
        )
        await self.__bot.vc.play(discord.FFmpegPCMAudio(file))

    @join.error
    @leave.error
    async def join_leave_error(self, interaction: Interaction, error):
        if isinstance(error, UserNotConnected):
            await self.send_error(interaction, 'Utente non connesso ad un canale vocale')
        elif isinstance(error, BotNotConnected):
            await self.send_error(interaction, 'Bot non presente nel canale vocale')
        elif isinstance(error, BotAlreadyConnected):
            await self.send_error(interaction, 'Bot già connesso ad un canale vocale')
        elif isinstance(error, UserNotInBotVc):
            await self.send_error(interaction, 'Utente non connesso al canale vocale del bot')
        else:
            print(error)

    @play.error
    async def play_error(self, interaction: Interaction, error):
        if isinstance(error, InexistentSkin):
            await self.send_error(interaction, 'Skin non esistente.')
        elif isinstance(error, InexistentVGS):
            await self.send_error(interaction, 'Vgs non esistente.')
        elif isinstance(error, MissingVGS):
            await self.send_error(interaction, 'Vgs mancante.')
        elif isinstance(error, UserNotConnected):
            await self.send_error(interaction, 'Utente non connesso ad un canale vocale')
        elif isinstance(error, BotNotConnected):
            await self.send_error(interaction, 'Bot non presente nel canale vocale')
        elif isinstance(error, UserNotConnected):
            await self.send_error(interaction, 'Utente non connesso ad un canale vocale')
        else:
            print(error)


async def setup(bot: ext.commands.Bot):
    await bot.add_cog(VoiceChannelCog(bot))
