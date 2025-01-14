import os

from discord import Embed, Colour, File, Member


class EmbedFactory:
    def __init__(self) -> None:
        self.__name_bot = "Tyr"
        self.__icon_url = "https://webcdn.hirezstudios.com/smite/god-icons/tyr.jpg"
        self.__icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')

    def error(self, error: str = " ") -> Embed:
        embed = Embed(title=" ", description="***"+error+"***", colour=Colour.red())
        embed.set_author(name=self.__name_bot, icon_url=self.__icon_url)
        return embed

    def embed(self, mess: str = " ", author: Member = None) -> Embed:
        embed = Embed(title=mess, colour=Colour.blue())
        embed.set_author(name=self.__name_bot, icon_url=self.__icon_url)
        if author:
            embed.set_footer(text=author.display_name, icon_url=author.avatar.url)
        return embed
