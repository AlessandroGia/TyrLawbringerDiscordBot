from typing import Any, Optional

from discord import app_commands, Interaction, Member
from discord.ext.commands import Command

from src.voice_state.voicelines import VoiceLines


def autocomplete_value(members: list[Member], value: str) -> list[app_commands.Choice]:
    members = [
        member for member in (members if value else members[:25])
        if not value or value.lower() in member.name.lower() or value.lower() in member.display_name.lower()
    ][:25]

    return [
        app_commands.Choice(name=member.display_name,value=str(member.id))
        for member in members
    ]


class GuildUsersVip(app_commands.Transformer):

        async def autocomplete(self, interaction: Interaction, value: str, /) -> list[app_commands.Choice]:
            members_in_vc: list[Member] = [
                member for channel in interaction.guild.voice_channels for member in channel.members
            ]
            members = members_in_vc + [member for member in interaction.guild.members if member not in members_in_vc]

            return autocomplete_value(members, value)

        async def transform(self, interaction: Interaction, value: str, /) -> Member:
            member = interaction.guild.get_member(int(value))
            if not member:
                raise
            return member


class GuildUsers(app_commands.Transformer):

    async def autocomplete(self, interaction: Interaction, value: str, /) -> list[app_commands.Choice]:
        return autocomplete_value(list(interaction.guild.members), value)

    async def transform(self, interaction: Interaction, value: str, /) -> Member:
        member = interaction.guild.get_member(int(value))
        if not member:
            raise
        return member

class ChannelUsers(app_commands.Transformer):

    async def autocomplete(self, interaction: Interaction, value: str, /) -> list[app_commands.Choice]:
        return autocomplete_value(list(interaction.channel.members), value)

    async def transform(self, interaction: Interaction, value: str, /) -> Member:
        member = interaction.guild.get_member(int(value))
        if not member:
            raise
        return member

class Skins(app_commands.Transformer):

    def __init__(self):
        voice_lines: VoiceLines = VoiceLines()
        self.__skins: dict = voice_lines.get_skins_name()

    async def autocomplete(self, interaction: Interaction, value: str, /) -> list[app_commands.Choice]:
        return [
            app_commands.Choice(name=skin_name, value=skin)
            for skin, skin_name in self.__skins.items()
            if not value or value.lower() in skin_name.lower
        ]

    async def transform(self, interaction: Interaction, value: str, /) -> str:
        return value