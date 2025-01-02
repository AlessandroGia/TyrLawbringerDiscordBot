import random

class Gifs:

    justice: list = [
        "https://tenor.com/it/view/smite-moba-tyr-warrior-solo-gif-8065517919568960367",
        "https://tenor.com/qspo5lcQorH.gif",
        "https://tenor.com/it/view/smite-moba-tyr-warrior-solo-gif-8854261619111342866"
    ]

    op: list = [
        "https://tenor.com/it/view/spl-deathwalker-tyr-smite-ankara-gif-26459982"
    ]

class Quotes:

    quotes_on_join: list = [
        "HAI!"
    ]

    quotes_on_leave: list = [
        "No, that's no.",
        "That's no funny.",
        "Idiocy is not a defense.",
        "You cannot stop justice!",
        "Begone foul creature!",
        "The wicked fall before me!",
    ]

    quotes_on_ban: list = [
        "We don't have time for jokes!",
        "You chose this, remember that.",
        "I take no joy in what must be done!"
    ]

    quotes_on_ping: list = [
        "We don't have time for jokes!",
        "Idiocy is not a defense.",
        "I take no joy in what must be done!",
        "That\'s no funny."
    ]

    @staticmethod
    def get_random(_list: list):
        return random.choice(_list)
