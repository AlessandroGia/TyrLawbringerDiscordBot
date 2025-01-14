
from discord import app_commands, utils, Interaction, VoiceChannel, VoiceProtocol

from config import Config
from src.exceptions.VoiceChannelExceptions import *

config = Config()

def __channel_connected_to(interaction: Interaction) -> VoiceProtocol | None:
    return utils.get(interaction.client.voice_clients, guild=interaction.guild)

def __get_channel_by_id(interaction: Interaction, channel_id: int) -> VoiceChannel:
    return utils.get(interaction.guild.voice_channels, id=channel_id)


def check_voice_channel():
    def predicate(interaction: Interaction) -> bool:

        private_channel: VoiceChannel = __get_channel_by_id(interaction, int(config.get('channels.private')))

        if not interaction.user.voice:
            raise UserNotConnected

        if interaction.command.name == 'join':

            if __channel_connected_to(interaction) and __channel_connected_to(interaction).channel != private_channel:
                raise BotAlreadyConnected

        else:
            if (not __channel_connected_to(interaction) or
                    (__channel_connected_to(interaction).channel == private_channel and interaction.user.voice.channel != private_channel)
            ):
                raise BotNotConnected

            if not interaction.user.voice.channel == __channel_connected_to(interaction).channel:
                raise UserNotInBotVc

        return True
    return app_commands.check(predicate)
