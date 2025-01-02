from discord import Embed, Colour

class EmbedFactory:
    def __init__(self) -> None:
        self.__name_bot = "Susano"
        self.__icon_url = "https://webcdn.hirezstudios.com/smite/god-icons/tyr.jpg"

    def error(self, error: str = " ") -> Embed:
        embed = Embed(title=" ", description="***"+error+"***", colour=Colour.red())
        embed.set_author(name=self.__name_bot, icon_url=self.__icon_url)
        return embed

    def embed(self, mess: str = " ", title: str = " ", footer: str = " ") -> Embed:
        embed = Embed(title=title, description=mess.replace(", Default", ""), colour=Colour.blue())
        embed.set_author(name=self.__name_bot, icon_url=self.__icon_url)
        embed.set_footer(text=footer)
        return embed
