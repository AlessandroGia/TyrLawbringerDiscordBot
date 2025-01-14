from discord.app_commands import AppCommandError

class MissingVGS(AppCommandError):
    pass


class InexistentVGS(AppCommandError):
    pass


class InexistentSkin(AppCommandError):
    pass
