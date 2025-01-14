from discord import Guild
from discord import Member, VoiceChannel


class VoiceGuildData:
    def __init__(self):
        self.__temp_channels_names = {'Gi', 'Yu', 'Jin', 'Rei', 'Makoto', 'Meiyo', 'Chugi'}
        self.__private: list[Member] = []
        self.__temp_channels: list[VoiceChannel] = []

    def add_member_to_private(self, user: Member):
        self.__private.append(user)

    def pop_member_in_private(self, user: Member) -> bool:
        if user in self.__private:
            self.__private.remove(user)
            return True
        return False

    def max_channels(self) -> bool:
        return len(self.__temp_channels_names) == len(self.__temp_channels)

    def num_temp_channels(self) -> int:
        return len(self.__temp_channels)

    async def new_temp_channel(self, guild: Guild, channels: list[VoiceChannel]):
        existing_channel_names = {channel.name for channel in channels}
        for channels_name in self.__temp_channels_names:
            if channels_name not in existing_channel_names:
                new_channel = await guild.create_voice_channel(channels_name)
                self.__temp_channels.append(new_channel)
                break

    async def remove_temp_channel(self):
        for channel in self.__temp_channels:
            if not channel.members:
                await channel.delete()
                self.__temp_channels.remove(channel)
                break