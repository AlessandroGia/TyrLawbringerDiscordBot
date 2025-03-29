import asyncio

from discord import Message, File, Interaction, Member, Role, TextChannel
from discord.ext import commands

from src.modules.leveling.stats_info import STATS
from src.modules.leveling.images import Images
from src.db.db import DB

import io

from config import waiting_typing


class Exping:
    def __init__(self, bot) -> None:
        self.__bot: commands.Bot = bot
        self.__images: Images = Images()
        self.__db: DB = DB()
        self.__roles_id: set = set(STATS.values())

    async def get_user_points(self, guild_id: int, user_id: int):
        return self.__db.get_user_points_db(guild_id, user_id)

    async def set_user_points(self, guild_id: int, user: Member, points: int):
        self.__db.set_user_points_db(guild_id, user.id, points)
        await self.__check_role(guild_id, user)

    async def exp(self, mess: Message):
        self.__db.increment_user_points_db(mess.guild.id, mess.author.id,1)
        if role_id := await self.__check_role(mess.guild.id, mess.author):
            await self.__send_lvl_up(mess.channel, mess.author, mess.guild.get_role(role_id))

    def __points_to_next_lvl(self, guild_id: int, user_id: int):
        points = self.__db.get_user_points_db(guild_id, user_id)

        for k in STATS.keys():
            if points < k:
                return k - points

        return -1

    async def __remove_old_roles(self, user: Member):
        roles_to_remove = {role.id for role in user.roles} & self.__roles_id

        if roles_to_remove:
            for role in roles_to_remove:
                await user.remove_roles(self.__bot.get_guild(user.guild.id).get_role(role))

    @staticmethod
    async def __add_new_role(user: Member, role: Role):
        await user.add_roles(role)

    async def __update_roles(self, user: Member, role: Role):
        await self.__remove_old_roles(user)
        await self.__add_new_role(user, role)

    async def __check_role(self, guild_id: int, user: Member) -> int:
        points = self.__db.get_user_points_db(guild_id, user.id)
        role_id = self.__get_role_by_points(points)
        all_user_roles = {role.id for role in user.roles} - {role_id}

        if not role_id:
            await self.__remove_old_roles(user)
        elif role_id not in {role.id for role in user.roles} or any(role in all_user_roles for role in self.__roles_id):
            await self.__update_roles(user, self.__bot.get_guild(guild_id).get_role(role_id))
            return role_id

        return False

    @staticmethod
    def __get_role_by_points(points: int):
        role_id = None

        for threshold, role in STATS.items():
            if points >= threshold:
                role_id = role
            else:
                break

        return role_id

    async def __send_lvl_up(self, channel: TextChannel, author: Member, role: Role) -> None:
        img = self.__images.create_image(role, author.name)
        content = f'{author.mention} Nice Job!'

        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = File(image_binary, 'level.png')
            async with channel.typing():
                await asyncio.sleep(waiting_typing(content))
            await channel.send(content=content, file=file)

    def get_roles_and_points_to_lvl(self, interaction: Interaction):
        points = self.__db.get_user_points_db(
            interaction.guild.id,
            interaction.user.id
        )
        current_role = None
        role_after = None
        points_to_lvl = 0

        for k, v in STATS.items():
            if points >= k:
                current_role = v
            else:
                role_after = v
                points_to_lvl = k - points
                break

        guild_roles = interaction.guild.roles
        current_role_obj = next((role for role in guild_roles if role.id == current_role), None)
        role_after_obj = next((role for role in guild_roles if role.id == role_after), None)

        return current_role_obj, role_after_obj, points_to_lvl
