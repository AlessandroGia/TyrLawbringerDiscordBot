import discord
from discord import ext, Object, Member, VoiceState, VoiceClient, app_commands, Interaction, VoiceChannel
from discord.app_commands import Transform
from discord.ext import commands, tasks

from src.custom_transformers.custom_transformers import GuildUsersVip, GuildUsers
from src.voice_state.CQueue import CQueue

from src.embed.embed import EmbedFactory
from src.voice_state.CVoiceState import CVoiceState
from src.voice_state.events.VoiceclientEvents import Join, Leave
from src.voice_state.voice_guild_data import VoiceGuildData


class VoiceChannelCog(ext.commands.Cog):


    def __init__(self, bot: ext.commands.Bot):
        self.__bot = bot
        self.__voice_state = CVoiceState(bot)
        self.__queue = CQueue()
        self.__embed = EmbedFactory()

        self.__prive_channel: int = 988927976731185223
        self.__inactivity_channel: int = 992433995696578682

        self.__voice_guild_data: dict[int, VoiceGuildData] = {}

    def __get_voice_guild_data(self, guild_id: int) -> VoiceGuildData:
        if guild_id not in self.__voice_guild_data:
            self.__voice_guild_data[guild_id] = VoiceGuildData()
        return self.__voice_guild_data[guild_id]

    async def __check_user_and_move(self, member: Member) -> None:
        if self.__get_voice_guild_data(member.guild.id).pop_member_in_prive(member):
            channel: VoiceChannel = member.guild.get_channel(self.__prive_channel)
            if member.voice and member.voice.channel != channel:
                await member.move_to(channel)

    async def __check_temp_channels(self, member: Member) -> None:
        channels: list[VoiceChannel] = [
            channel for channel in member.guild.voice_channels
            if channel.id != self.__prive_channel and channel.id != self.__inactivity_channel
        ]
        guild_data: VoiceGuildData = self.__get_voice_guild_data(member.guild.id)
        empty_channels: list[VoiceChannel] = [channel for channel in channels if not channel.members]

        if not empty_channels and not guild_data.max_channels():
            await guild_data.new_temp_channel(member.guild, channels)
        elif len(empty_channels) > 1 and guild_data.num_temp_channels() > 0:
            await guild_data.remove_temp_channel()

    @ext.commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if not before.channel and after.channel:
            await self.__check_user_and_move(member)

        if before.channel != after.channel:
            await self.__check_temp_channels(member)


    @app_commands.command(
        name='prive',
        description='Fa joinare l\'utente al canale privato.'
    )
    @commands.is_owner()
    async def prive(self, interaction: Interaction, user: Transform[discord.Member, GuildUsersVip]) -> None:
        channel: VoiceChannel = interaction.guild.get_channel(self.__prive_channel)
        if user.voice and user.voice.channel != channel:
            await user.move_to(channel)
            await interaction.response.send_message(
                f'{user.display_name} è stato spostato nel canale privato.',
                ephemeral=True
            )
        else:
            self.__get_voice_guild_data(interaction.guild_id).add_member_to_prive(user)
            await interaction.response.send_message(
                f'{user.display_name} è stato aggiunto alla lista del canale privato.',
                ephemeral=True
            )

    @app_commands.command(
        name='prive-remove',
        description='Rimuove l\'utente dalla lista canale privato.'
    )
    @commands.is_owner()
    async def prive_remove(self, interaction: Interaction, user: Transform[discord.Member, GuildUsers]) -> None:
        if self.__get_voice_guild_data(interaction.guild_id).pop_member_in_prive(user):
            await interaction.response.send_message(
                f'{user.display_name} è stato rimosso dalla lista del canale privato.',
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f'{user.display_name} non è presente nella lista del canale privato.',
                ephemeral=True
            )

async def setup(bot: ext.commands.Bot):
    await bot.add_cog(VoiceChannelCog(bot), guilds=[Object(id=928785387239915540)])
