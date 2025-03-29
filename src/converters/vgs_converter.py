from discord import app_commands, Interaction

from src.modules.voice_state.voicelines import VoiceLines


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