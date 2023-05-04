import random
class Quotes:

    quotes_on_leave: list = [
        "No, that's no.", "That\'s no funny.", "Idiocy is not a defense.", "You cannot stop justice!",
        "Begone foul creature!", "The wicked fall before me!",
    ]

    quotes_on_join: list = [
        "HAI!"
    ]

    quotes_on_ban: list = [
        "We don't have time for jokes!", "You chose this, remember that.",
        "I take no joy in what must be done!"
    ]

    @staticmethod
    def get_random(_list: list):
        return random.choice(_list)

