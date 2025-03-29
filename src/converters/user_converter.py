from discord import app_commands, Interaction, Member


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
