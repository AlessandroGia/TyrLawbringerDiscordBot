from discord import Colour, Embed as embed


class Embed:
    def __init__(self) -> None:
        self.__name_bot = "Susano"
        self.__icon_url = "https://webcdn.hirezstudios.com/smite/god-icons/tyr.jpg"
        pass

    def error(self, error: str = " ") -> embed:
        emb = embed(title=" ", description="***"+error+"***", colour=Colour.red())
        emb.set_author(name=self.__name_bot, icon_url=self.__icon_url)
        return emb

    def embed(self, mess: str = " ", title: str = " ", footer: str = " ") -> embed:
        emb = embed(title=title, description=mess.replace(", Default", ""), colour=Colour.blue())
        emb.set_author(name=self.__name_bot, icon_url=self.__icon_url)
        emb.set_footer(text=footer)
        return emb
