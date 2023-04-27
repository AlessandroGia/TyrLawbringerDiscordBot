from __future__ import annotations

import discord
from discord import Message, File, Interaction, Member, Guild
from PIL import Image, ImageDraw, ImageFont

import redis
import io
import os


class StatsXp:

    def __init__(self) -> None:

        self.__redis = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )
        #self.__set_user_points_db(518039812607967265, 928785387239915540, 0)
        self.__roles_id = [stat['id_role'] for stat in self.__STATS.values()]
        self.__tree = {}
        self.__root = os.path.dirname(os.path.abspath(__file__))
        self.__load_images()

    def __load_images(self) -> None:
        self.__img_grandmaster = Image.open(os.path.join(self.__root, 'RanksSymbols', '1a.png'))
        self.__img_master = Image.open(os.path.join(self.__root, 'RanksSymbols', '2a.png'))
        self.__img_diamond = Image.open(os.path.join(self.__root, 'RanksSymbols', '3a.png'))
        self.__img_platinum = Image.open(os.path.join(self.__root, 'RanksSymbols', '4a.png'))
        self.__img_gold = Image.open(os.path.join(self.__root, 'RanksSymbols', '5a.png'))
        self.__img_silver = Image.open(os.path.join(self.__root, 'RanksSymbols', '6a.png'))
        self.__img_bronze = Image.open(os.path.join(self.__root, 'RanksSymbols', '7a.png'))

    def __get_user_points_form_db(self, id_user: int, id_guild: int) -> int:
        if user := self.__redis.hgetall(str(id_user)):
            return int(user[str(id_guild)])
        return 0

    def __set_user_points_db(self, id_user: int, id_guild: int, points: int) -> None:
        self.__redis.hset(
            str(id_user),
            mapping={id_guild: points}
        )

    def __add_point(self, id_user: int, id_guild: int) -> None:
        self.__tree[id_user][id_guild]['points'] += 1
        self.__set_user_points_db(
            id_user,
            id_guild,
            points=self.__tree[id_user][id_guild]['points']
        )

    def __get_index(self, points: int) -> int:
        for x in self.__STATS:
            if x == 27 or points < self.__STATS[x + 1]['points']:
                return x

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
            if points_db := self.__get_user_points_form_db(id_user, id_guild):
                self.__tree[id_user][id_guild]['points'] = points_db
                self.__tree[id_user][id_guild]['index'] = self.__get_index(points_db)
            else:
                self.__tree[id_user][id_guild]['points'] = 0
                self.__tree[id_user][id_guild]['index'] = 0
                self.__set_user_points_db(id_user, id_guild, 0)

    async def __delete_old_role(self, user: Member, guild: Guild) -> None:
        for role in self.__roles_id:
            if role and user.get_role(role):
                await user.remove_roles(guild.get_role(role))

    async def __change_role(self, user: Member, guild: Guild, i: int) -> None:
        await self.__delete_old_role(user, guild)
        if i:
            await user.add_roles(guild.get_role(self.__STATS[i]['id_role']))

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
        self.__set_user_points_db(id_user, interaction.guild.id, points)
        index = self.__get_index(points)
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
        index = self.__get_index(self.__tree[ctx.author.id][ctx.guild.id]['points'])
        if index != self.__tree[ctx.author.id][ctx.guild.id]['index']:
            self.__tree[ctx.author.id][ctx.guild.id]['index'] = index
            await self.__send_lvl_up(ctx, index)
            await self.__change_role(ctx.author, ctx.guild, index)

    async def __send_lvl_up(self, ctx: Message, index: int) -> None:
        role_name = ctx.guild.get_role(self.__STATS[index]['id_role']).name
        user_name = ctx.author.name
        img = self.__create_image(role_name, user_name, index)
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
            role_name = interaction.guild.get_role(self.__STATS[index]['id_role']).name
            if points := kwargs.get('points'):
                role_name += f' - {points}pt.'
            user_name = user.name
            img = self.__create_image(role_name, user_name, index)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                content = user.mention
                if index < 27:
                    content += f" ***{self.__STATS[int(self.__tree[user_id][guild_id]['index']) + 1]['points'] - self.__tree[user_id][guild_id]['points']}pt.*** left to rank up to **{interaction.guild.get_role(self.__STATS[index + 1]['id_role']).name}**."
                await interaction.response.send_message(
                    content=content,
                    file=File(fp=image_binary, filename='image.png')
                )
        else:
            await interaction.response.send_message(
                content=f"{user.mention} ***{self.__STATS[int(self.__tree[user_id][guild_id]['index']) + 1]['points'] - self.__tree[user_id][guild_id]['points']}pt.*** left to rank up to **{interaction.guild.get_role(self.__STATS[index + 1]['id_role']).name}**."
            )

    def __create_image(self, role_name: str, user_name: str, index: int):
        len_name, len_rank = len(user_name) * 10, len(role_name) * 6
        len_w = len_name if len_name > len_rank else len_rank
        img, rgb = self.__get_image_color_rank(index)
        img_w, img_h = img.size
        image = Image.new('RGBA', (150 + len_w, img_h), rgb)
        font_color = tuple([x - j for x, j in zip((255, 255, 255), rgb)])
        smite_font = ImageFont.truetype(os.path.join(self.__root, 'Font', 'PenumbraHalfSerifStd-SeBd.otf'), 15)
        l_user = ImageDraw.Draw(image)
        l_user.text((img_w + 10, 10), user_name, font=smite_font, fill=font_color)
        smite_font = ImageFont.truetype(os.path.join(self.__root, 'Font', 'PenumbraHalfSerifStd-Bold.otf'), 10)
        l_rank = ImageDraw.Draw(image)
        l_rank.text((img_w + 10, img_h - 20), role_name, font=smite_font, fill=font_color)
        image.paste(img)
        return image

    def __get_image_color_rank(self, index: int) -> (Image, (int, int, int)):
        if 1 <= index <= 5:
            return self.__img_bronze, (205, 127, 50)
        elif 6 <= index <= 10:
            return self.__img_silver, (192, 192, 192)
        elif 11 <= index <= 15:
            return self.__img_gold, (255, 215, 0)
        elif 16 <= index <= 20:
            return self.__img_platinum, (229, 228, 226)
        elif 21 <= index <= 25:
            return self.__img_diamond, (185, 242, 255)
        elif index == 26:
            return self.__img_master, (138, 43, 226)
        elif index == 27:
            return self.__img_grandmaster,  (255, 255, 255)
        else:
            return '', (0, 0, 0)

    __STATS = {
        0: {
            'points': 0,
            'id_role': None
        },
        1: {
            'points': 100,
            'id_role': 1099149090744451073
        },
        2: {
            'points': 200,
            'id_role': 1099149715964174416
        },
        3: {
            'points': 300,
            'id_role': 1099149782930423898
        },
        4: {
            'points': 400,
            'id_role': 1099149889428017172
        },
        5: {
            'points': 500,
            'id_role': 1099149965697232967
        },
        6: {
            'points': 620,
            'id_role': 1099844523015798904
        },
        7: {
            'points': 740,
            'id_role': 1099844779044524103
        },
        8: {
            'points': 860,
            'id_role': 1099844840780472404
        },
        9: {
            'points': 980,
            'id_role': 1099844909747421274
        },
        10: {
            'points': 1100,
            'id_role': 1099844958686560256
        },
        11: {
            'points': 1240,
            'id_role': 1099845211452092456
        },
        12: {
            'points': 1380,
            'id_role': 1099845258638000199
        },
        13: {
            'points': 1520,
            'id_role': 1099845304125243483
        },
        14: {
            'points': 1660,
            'id_role': 1099845439404130385
        },
        15: {
            'points': 1800,
            'id_role': 1099845486254510250
        },
        16: {
            'points': 1960,
            'id_role': 1099845491409297408
        },
        17: {
            'points': 2120,
            'id_role': 1099845992569897051
        },
        18: {
            'points': 2280,
            'id_role': 1099846055350243369
        },
        19: {
            'points': 2440,
            'id_role': 1099846117811830924
        },
        20: {
            'points': 2600,
            'id_role': 1099846162506322010
        },
        21: {
            'points': 2780,
            'id_role': 1099847219311554620
        },
        22: {
            'points': 2960,
            'id_role': 1099847470630047816
        },
        23: {
            'points': 3140,
            'id_role': 1099847531715891291
        },
        24: {
            'points': 3320,
            'id_role': 1099847572794908692
        },
        25: {
            'points': 3500,
            'id_role': 1099847620983263262
        },
        26: {
            'points': 3700,
            'id_role': 1099847997166194792
        },
        27: {
            'points': 4000,
            'id_role': 1099848295909707818
        },

    }

