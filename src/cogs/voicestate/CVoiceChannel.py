from __future__ import annotations

from discord import ext, Object, Member, VoiceState, VoiceClient
from discord.ext import commands, tasks

from .CVoiceState import CVoiceState
from .events.VoiceclientEvents import *
from src.cogs.voicestate.CQueue import CQueue
import asyncio


class CVoiceChannel(ext.commands.Cog):
    # {'member': member, 'state': state}
    #TODO: Fare una coda asincrona che tiene conto le varie operazione che il bot deve fare
    def __init__(self, bot: ext.commands.Bot):
        #self.__voice_state = CVoiceState(bot.loop)
        self.__queue = CQueue()
        self.__vc: VoiceClient | None = None
        self.__bot = bot
        #self.__run.start()

    def cog_unload(self):
        self.__run.cancel()

    @tasks.loop()
    async def __run(self):
        while True:
            print('Waiting')
            element = await asyncio.wait_for(self.__queue.get(), timeout=None)
            print('Event!')
            await self.__on_user_event(element['state'], element['event'])

    async def __on_user_event(self, state: VoiceState, event: Join | Leave):
        print('1')
        if state.channel.members:
            print('2')
            if self.__bot.application.id not in [m.id for m in state.channel.members]:
                await self.__voice_state.join(state.channel)

    async def __join(self, state):
        self.__vc = await state.channel.connect()

    def __add_event(self, member: Member, before: VoiceState, after: VoiceState):
        print('Add')
        if not before.channel and after.channel:
            state = after
            event = Join()
            print(' Join')
        elif before.channel and not after.channel:
            state = before
            event = Leave()
            print(' Leave')
        else:
            return None

        self.__queue.add({
            'state': state,
            'event': event
        })


async def setup(bot: ext.commands.Bot):
    await bot.add_cog(CVoiceChannel(bot), guilds=[Object(id=928785387239915540)])
