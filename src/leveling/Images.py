import os
from PIL import Image, ImageDraw, ImageFont
from discord import Role
from src.leveling.StatsInfo import STATS


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

    def create_image(self, role: Role, user_name: str) -> Image:
        len_name, len_rank = len(user_name) * 10, len(role.name) * 6
        len_w = len_name if len_name > len_rank else len_rank
        img, rgb = self.__get_image_color_rank_by_index(
            list(STATS.values()).index(role.id)
        )
        img_w, img_h = img.size
        image = Image.new('RGBA', (150 + len_w, img_h), rgb)
        font_color = tuple([x - j for x, j in zip((255, 255, 255), rgb)])
        smite_font = ImageFont.truetype(os.path.join(self.__root, 'font', 'PenumbraHalfSerifStd-SeBd.otf'), 15)
        l_user = ImageDraw.Draw(image)
        l_user.text((img_w + 10, 10), user_name, font=smite_font, fill=font_color)
        smite_font = ImageFont.truetype(os.path.join(self.__root, 'font', 'PenumbraHalfSerifStd-Bold.otf'), 10)
        l_rank = ImageDraw.Draw(image)
        l_rank.text((img_w + 10, img_h - 20), role.name, font=smite_font, fill=font_color)
        image.paste(img)
        return image

    def __get_image_color_rank_by_index(self, index: int) -> (Image, (int, int, int)):
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

