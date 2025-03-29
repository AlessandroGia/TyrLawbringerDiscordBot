import os

from src.exceptions.vgs_exceptions import InexistentVGS, MissingVGS, InexistentSkin
from random import choice


class VoiceLines:
    def __init__(self):
        self.__voice_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'audio', 'tyr')

    def get_skins_name(self) -> dict[str, str]:
        skins = {}

        for skin in os.listdir(self.__voice_dir):
            skin_name = skin.replace('_', ' ').removesuffix(' tyr').capitalize()
            skins[skin] = skin_name
        skins['default'] = 'Tyr'

        return skins

    def join(self):
        return self.get_ogg('default', 'vvgh')

    def leave(self):
        return self.get_ogg('default', 'vvgb')

    def get_ogg(self, skin, voice_line) -> str:
        skin_dir = os.path.join(self.__voice_dir, skin)
        if not os.path.exists(skin_dir):
            raise InexistentSkin
        vgs_dir = os.path.join(skin_dir, voice_line)
        if not os.path.exists(vgs_dir):
            raise InexistentVGS
        files = os.listdir(vgs_dir)
        if not files:
            raise MissingVGS

        return os.path.join(vgs_dir, choice([f for f in files if f.endswith('.ogg')]))

