from asyncio import AbstractEventLoop

from discord import VoiceClient, VoiceChannel, VoiceProtocol

from src.voicestate.events.VoiceclientEvents import *


class CVoiceState:
    def __init__(self, loop: AbstractEventLoop):
        self.__loop: AbstractEventLoop = loop
        self.__vc: VoiceClient | None = None

    def connected(self):
        return self.__vc and self.__vc.is_connected()

    async def disconnect(self):
        if self.connected():
            await self.__vc.disconnect()

    async def channel_event(self, channel: VoiceChannel, event: Join | Leave):
        self.__vc = channel
        vc = channel.guild.voice_client
        print(vc.is_connected())
        if isinstance(event, Join):
            ...
        elif isinstance(event, Leave):
            ...

        if not vc or not vc.is_connected():
            await self.__vc.connect()
        else:
            await vc.move_to(channel)