from asyncio import AbstractEventLoop

from discord import VoiceClient, VoiceChannel


class CVoiceState:
    def __init__(self, loop: AbstractEventLoop):
        self.__loop: AbstractEventLoop = loop
        self.__vc: VoiceClient | None = None

    def connected(self):
        return self.__vc and self.__vc.is_connected()

    def __connect(self, channel: VoiceChannel):
        print('A')
        if not self.__vc or not self.__vc.is_connected():
            print('B')
            self.__vc = self.__loop.create_task(channel.connect())
            self.__vc.cancel()
            self.__vc.done()



    async def disconnect(self):
        if self.is_connected():
            await self.__vc.disconnect()

    async def join(self, channel: VoiceChannel):
        print('-----', self.__vc)
        if not self.__vc or not self.__vc.is_connected():
            print('3')
            self.__connect(channel)
            print('4')
        else:
            print('5')
            await self.__vc.move_to(channel)
            print('6')