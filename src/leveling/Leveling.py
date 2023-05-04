from discord import Message, File, Interaction, Member, Guild

from src.leveling.StatsInfo import StatsInfo
from src.leveling.Images import Images
from src.Idb import Idb

import io


class Leveling:
    def __init__(self) -> None:
        self.__stats = StatsInfo()
        self.__images = Images()
        self.__db = Idb()
        self.__roles_id = self.__stats.get_all_roles_id()
        self.__tree = {}

    async def get_user_points(self, interaction: Interaction):
        self.__update_user_points(interaction.user.id, interaction.guild.id)
        await self.__send_mess(
            interaction,
            self.__tree[interaction.user.id][interaction.guild.id]['index'],
            points=self.__tree[interaction.user.id][interaction.guild.id]['points']
        )

    async def set_user_points(self, interaction: Interaction, id_user: int, points: int):
        member = interaction.guild.get_member(id_user)
        self.__update_user_points(id_user, interaction.guild.id)
        self.__db.set_user_points_db(id_user, interaction.guild.id, points)
        index = self.__stats.get_index_by_points(points)
        self.__tree[id_user][interaction.guild.id]['points'] = points
        self.__tree[id_user][interaction.guild.id]['index'] = index
        await self.__change_role(
            member,
            interaction.guild,
            self.__tree[id_user][interaction.guild.id]['index']
        )
        await self.__send_mess(
            interaction,
            index,
            user=member
        )

    async def exp(self, ctx: Message) -> None:
        self.__update_user_points(ctx.author.id, ctx.guild.id)
        self.__add_point(ctx.author.id, ctx.guild.id)
        index = self.__stats.get_index_by_points(self.__tree[ctx.author.id][ctx.guild.id]['points'])
        if index != self.__tree[ctx.author.id][ctx.guild.id]['index']:
            self.__tree[ctx.author.id][ctx.guild.id]['index'] = index
            await self.__send_lvl_up(ctx, index)
            await self.__change_role(ctx.author, ctx.guild, index)

    def __add_point(self, id_user: int, id_guild: int) -> None:
        self.__tree[id_user][id_guild]['points'] += 1
        self.__db.set_user_points_db(
            id_user,
            id_guild,
            self.__tree[id_user][id_guild]['points']
        )

    def __update_user_points(self, id_user: int, id_guild: int) -> None:
        if not self.__tree.get(id_user) or not self.__tree[id_user].get(id_guild):
            if not self.__tree.get(id_user):
                self.__tree[id_user] = {}
                self.__tree[id_user][id_guild] = {}
                self.__tree[id_user][id_guild]['points'] = 0
                self.__tree[id_user][id_guild]['index'] = 0
            elif not self.__tree[id_user].get(id_guild):
                self.__tree[id_user][id_guild] = {}
                self.__tree[id_user][id_guild]['points'] = 0
                self.__tree[id_user][id_guild]['index'] = 0
            if points_db := self.__db.get_user_points_form_db(id_user, id_guild):
                self.__tree[id_user][id_guild]['points'] = points_db
                self.__tree[id_user][id_guild]['index'] = self.__stats.get_index_by_points(points_db)
            else:
                self.__tree[id_user][id_guild]['points'] = 0
                self.__tree[id_user][id_guild]['index'] = 0
                self.__db.set_user_points_db(id_user, id_guild, 0)

    async def __delete_old_role(self, user: Member, guild: Guild) -> None:
        for role in self.__roles_id:
            if role and user.get_role(role):
                await user.remove_roles(guild.get_role(role))

    async def __change_role(self, user: Member, guild: Guild, index: int) -> None:
        await self.__delete_old_role(user, guild)
        if index:
            await user.add_roles(guild.get_role(self.__stats.get_role_by_index(index)))

    async def __send_lvl_up(self, ctx: Message, index: int) -> None:
        role_name = ctx.guild.get_role(self.__stats.get_role_by_index(index)).name
        user_name = ctx.author.name
        img = self.__images.create_image(role_name, user_name, index)
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.channel.send(
                content=f'{ctx.author.mention} Nice Job!',
                file=File(fp=image_binary, filename='image.png')
            )

    async def __send_mess(self, interaction: Interaction, index: int, **kwargs):
        guild_id = interaction.guild.id
        user: Member = interaction.user
        if _user := kwargs.get('user'):
            user = _user
        user_id = user.id
        if index:
            role_name = interaction.guild.get_role(self.__stats.get_role_by_index(index)).name
            if points := kwargs.get('points'):
                role_name += f' - {points}pt.'
            user_name = user.name
            img = self.__images.create_image(role_name, user_name, index)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                content = user.mention
                if index < 27:
                    content += f" ***{self.__stats.get_points_by_index(self.__tree[user_id][guild_id]['index'] + 1) - self.__tree[user_id][guild_id]['points']}pt.*** left to rank up to **{interaction.guild.get_role(self.__stats.get_role_by_index(index + 1)).name}**."
                await interaction.response.send_message(
                    content=content,
                    file=File(fp=image_binary, filename='image.png')
                )
        else:
            await interaction.response.send_message(
                content=f"{user.mention} ***{self.__stats.get_points_by_index(self.__tree[user_id][guild_id]['index'] + 1) - self.__tree[user_id][guild_id]['points']}pt.*** left to rank up to **{interaction.guild.get_role(self.__stats.get_role_by_index(index + 1)).name}**."
            )


