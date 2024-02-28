import os
import discord


from asyncio import AbstractEventLoop

from discord import VoiceClient, VoiceChannel, Interaction, ext


from src.voicestate.PickLine import PickLine
from src.voicestate.events.VoiceclientEvents import *


class CVoiceState:
    def __init__(self, bot: ext.commands.Bot):
        self.__pick_line = PickLine()
        self.__loop: AbstractEventLoop = bot.loop
        self.__user = bot.user
        self.__vc: VoiceClient | None = None
        self.__root: str = os.path.dirname(os.path.realpath(__file__))
        print('AMDDADWDAX')

    async def join(self, interaction: Interaction):
        print('CISIA')
        self.__vc = await interaction.user.voice.channel.connect()
        print('a')
        self.__run.start()


    async def disconnect(self):
        await self.__vc.disconnect()
        self.__run.cancel()

    @ext.tasks.loop(seconds=10)
    async def __run(self):
        if self.__connected():
            await self.__playRandom()

    async def __playRandom(self):
        line, avatar = self.__pick_line.pick()
        try:
            source = discord.FFmpegPCMAudio(line)
            await self.__changePFP(avatar)
            self.__vc.play(source)
        except Exception as e:
            pass

    async def __changePFP(self, avatar: str):
        with open(avatar, 'rb') as image:
            await self.__user.edit(avatar=image.read())
    
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