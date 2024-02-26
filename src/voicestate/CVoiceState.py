import os
import discord


from asyncio import AbstractEventLoop

from discord import VoiceClient, VoiceChannel, Interaction

from src.voicestate.events.VoiceclientEvents import *


class CVoiceState:
    def __init__(self, loop: AbstractEventLoop):
        self.__loop: AbstractEventLoop = loop
        self.__vc: VoiceClient | None = None
        self.__root: str = os.path.dirname(os.path.realpath(__file__))

    async def join(self, interaction: Interaction):
        self.__vc = await interaction.user.voice.channel.connect()

    async def disconnect(self):
        await self.__vc.disconnect()

    
    def __connected(self):
        return self.__vc and isinstance(self.__vc, VoiceClient) and self.__vc.is_connected()

    async def __disconnect(self):
        if self.__connected():
            await self.__vc.disconnect()

    async def channel_event(self, channel: VoiceChannel, event: Join | Leave):

        if not self.__connected():
            self.__vc = await channel.connect()
        else:
            self.__vc.move_to(channel)

        if isinstance(event, Join):
            file = os.path.join(
                    self.__root, '..', 'voice', 'tyr', 'default', 'vvgh', 'Tyr_Other_G_H.ogg'
                )
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file))
            self.__vc.play(
                source
            )
        elif isinstance(event, Leave):
            ...