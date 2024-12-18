import os
from PIL import Image, ImageDraw, ImageFont
from discord import Role
from src.leveling.stats_info import STATS


class Images:
    def __init__(self) -> None:
        self.__root = os.path.dirname(os.path.abspath(__file__))
        self.__img_grandmaster = Image.open(os.path.join(self.__root, 'ranks_symbols', '1a.png'))
        self.__img_master = Image.open(os.path.join(self.__root, 'ranks_symbols', '2a.png'))
        self.__img_diamond = Image.open(os.path.join(self.__root, 'ranks_symbols', '3a.png'))
        self.__img_platinum = Image.open(os.path.join(self.__root, 'ranks_symbols', '4a.png'))
        self.__img_gold = Image.open(os.path.join(self.__root, 'ranks_symbols', '5a.png'))
        self.__img_silver = Image.open(os.path.join(self.__root, 'ranks_symbols', '6a.png'))
        self.__img_bronze = Image.open(os.path.join(self.__root, 'ranks_symbols', '7a.png'))

        self.__rank_map = {
            range(1, 6): (self.__img_bronze, (205, 127, 50)),
            range(6, 11): (self.__img_silver, (192, 192, 192)),
            range(11, 16): (self.__img_gold, (255, 215, 0)),
            range(16, 21): (self.__img_platinum, (229, 228, 226)),
            range(21, 26): (self.__img_diamond, (185, 242, 255)),
            26: (self.__img_master, (138, 43, 226)),
            27: (self.__img_grandmaster, (255, 255, 255))
        }

    def create_image(self, role: Role, user_name: str) -> Image:
        len_w = max(len(user_name) * 10, len(role.name) * 6)
        img, rgb = self.__get_image_color_rank_by_index(
            list(STATS.values()).index(role.id)
        )
        img_w, img_h = img.size
        image = Image.new('RGBA', (150 + len_w, img_h), rgb)
        font_color = tuple([x - j for x, j in zip((255, 255, 255), rgb)])
        smite_font_user = ImageFont.truetype(os.path.join(self.__root, 'font', 'PenumbraHalfSerifStd-SeBd.otf'), 15)
        smite_font_rank = ImageFont.truetype(os.path.join(self.__root, 'font', 'PenumbraHalfSerifStd-Bold.otf'), 10)
        draw = ImageDraw.Draw(image)
        draw.text((img_w + 10, 10), user_name, font=smite_font_user, fill=font_color)
        draw.text((img_w + 10, img_h - 20), role.name, font=smite_font_rank, fill=font_color)
        '''
        l_user = ImageDraw.Draw(image)
        l_user.text((img_w + 10, 10), user_name, font=smite_font, fill=font_color)
        l_rank = ImageDraw.Draw(image)
        l_rank.text((img_w + 10, img_h - 20), role.name, font=smite_font, fill=font_color)
        '''
        image.paste(img)
        return image

    def __get_image_color_rank_by_index(self, index: int) -> (Image, (int, int, int)):
        for key, value in self.__rank_map.items():
            if index in key:
                return value
        return '', (0, 0, 0)

