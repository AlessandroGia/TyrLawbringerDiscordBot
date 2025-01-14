from discord.app_commands import AppCommandError


class UserNotConnected(AppCommandError):
    pass


class BotAlreadyConnected(AppCommandError):
    pass


class BotNotConnected(AppCommandError):
    pass


class UserNotInBotVc(AppCommandError):
    pass
