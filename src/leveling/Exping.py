from discord import Message, File, Interaction, Member, Role
from discord.ext import commands

from src.leveling.StatsInfo import STATS
from src.leveling.Images import Images
from src.Idb import Idb

import discord
import io


class Exping:
    def __init__(self, bot) -> None:
        self.__bot: commands.Bot = bot
        self.__images: Images = Images()
        self.__db: Idb = Idb()
        self.__roles_id: set = set(STATS.values())

    async def get_user_points(self, guild_id: int, user_id: int):
        return self.__db.get_user_points_db(
            guild_id,
            user_id
        )

    async def set_user_points(self, guild_id: int, user: Member, points: int):
        self.__db.set_user_points_db(
            guild_id,
            user.id,
            points
        )
        await self.__check_role(
            guild_id,
            user
        )

    async def exp(self, mess: Message):
        self.__db.increment_user_points_db(
            mess.guild.id,
            mess.author.id,
            1
        )
        print('Checking role', mess.guild.id, mess.author)
        if role_id := await self.__check_role(mess.guild.id, mess.author):
            print('LVL UP!!! OFRAT')
            await self.__send_lvl_up(
                mess,
                mess.guild.get_role(role_id)
            )

    def __points_to_next_lvl(self, guild_id: int, user_id: int):
        points = self.__db.get_user_points_db(
            guild_id,
            user_id
        )
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
        await self.__add_new_role(
            user,
            role
        )

    async def __check_role(self, guild_id: int, user: Member) -> int:
        role_id = self.__get_role_by_points(
            self.__db.get_user_points_db(
                guild_id,
                user.id
            )
        )
        all_user_roles = {role.id for role in user.roles} - {role_id}
        if not role_id:
            await self.__remove_old_roles(user)

        elif role_id not in {role.id for role in user.roles} or any(role in all_user_roles for role in self.__roles_id):
            await self.__update_roles(
                user,
                self.__bot.get_guild(guild_id).get_role(role_id)
            )
            return role_id
        return False

    @staticmethod
    def __get_role_by_points(points: int):
        last = None
        for k, v in STATS.items():
            if points >= k:
                last = v
            else:
                break
        return last

    async def __send_lvl_up(self, ctx: Message, role: Role) -> None:
        img = self.__images.create_image(
            role,
            ctx.author.name
        )
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.channel.send(
                content=f'{ctx.author.mention} Nice Job!',
                file=File(fp=image_binary, filename='image.png')
            )

    def get_roles_and_points_to_lvl(self, interaction: Interaction):
        current_role = None
        role_after = None
        points_to_lvl = 0
        points = self.__db.get_user_points_db(
            interaction.guild.id,
            interaction.user.id
        )
        for k, v in STATS.items():
            if points >= k:
                current_role = v
            else:
                role_after = v
                points_to_lvl = k - points
                break
        return interaction.guild.get_role(current_role), interaction.guild.get_role(role_after), points_to_lvl
