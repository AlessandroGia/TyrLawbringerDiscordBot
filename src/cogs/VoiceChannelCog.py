
from discord import ext, Object, Member, VoiceState, VoiceClient, app_commands, Interaction
from discord.ext import commands, tasks

from src.exceptions.VoiceChannelExceptions import *
from src.voicestate.CQueue import CQueue
import asyncio

from src.checks.VoiceChannelChecks import check_voice_channel

from src.embed.Embed import Embed
from src.voicestate.CVoiceState import CVoiceState
from src.voicestate.events.VoiceclientEvents import Join, Leave


class VoiceChannelCog(ext.commands.Cog):
    # {'member': member, 'state': state}
    #TODO: Fare una coda asincrona che tiene conto le varie operazione che il bot deve fare
    def __init__(self, bot: ext.commands.Bot):
        self.__voice_state = CVoiceState(bot.loop)
        self.__queue = CQueue()
        self.__bot = bot
        self.__embed = Embed()


    @ext.commands.Cog.listener()
    async def on_ready(self):
        self.__run.start()


    @app_commands.command(
        name='start',
        description='start the tyring.'
    )
    @check_voice_channel()
    async def start(self, interaction: Interaction):
        await self.__voice_state.join(interaction)

    @app_commands.command(
        name='stop',
        description='stop the tyring.'
    )
    @check_voice_channel()
    async def stop(self, interaction: Interaction):
        await self.__voice_state.disconnect()


    def cog_unload(self):
        self.__run.cancel()

    @tasks.loop()
    async def __run(self):
        while True:
            element = await asyncio.wait_for(self.__queue.get(), timeout=None)
            await self.__on_user_event(element['state'], element['event'])

    async def __on_user_event(self, state: VoiceState, event: Join | Leave):
        if state.channel.members:
            if self.__bot.application.id not in [m.id for m in state.channel.members]:
                await self.__voice_state.channel_event(state.channel, event)


    @ext.commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        print(before, after)
        if not before.channel and after.channel:
            state = after
            event = Join()
        elif before.channel and not after.channel:
            state = before
            event = Leave()
        else:
            return None

        self.__queue.add({
            'state': state,
            'event': event
        })

    @stop.error
    async def leave_error(self, interaction: Interaction, error):
        if isinstance(error, UserNonConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei connesso a nessun canale vocale"), ephemeral=True, delete_after=5)
        elif isinstance(error, BotNonPresenteError):
            await interaction.response.send_message(embed=self.__embed.error("Il bot non e' connesso a nessun canale vocale"), ephemeral=True, delete_after=5)
        elif isinstance(error, UserNonStessoCanaleBotError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei nello stesso canale del bot"), ephemeral=True, delete_after=5)

    @start.error
    async def join_error(self, interaction: Interaction, error):
        if isinstance(error, UserNonConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei connesso a nessun canale vocale"), ephemeral=True, delete_after=5)
        elif isinstance(error, BotGiaConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Bot gia' connesso"), ephemeral=True, delete_after=5)

async def setup(bot: ext.commands.Bot):
    await bot.add_cog(VoiceChannelCog(bot), guilds=[Object(id=928785387239915540)])
