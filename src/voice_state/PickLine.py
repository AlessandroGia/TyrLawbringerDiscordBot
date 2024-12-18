import os
import random as rd

class PickLine:
    def __init__(self) -> None:
        self.__voice_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice', 'tyr')
        self.__image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')

    def pick(self) -> tuple[str, str]:
        line = ''
        avatar = ''
        while not line:
            skin = rd.choice(os.listdir(self.__voice_dir))
            line = self.__getLineBySkin(skin)
            avatar = os.path.join(self.__image_dir, skin + '.png')
        return line, avatar

    def __getLineBySkin(self, skin: str) -> str | None:
        voice_skin_dir = os.path.join(self.__voice_dir, skin)
        voiceline = rd.choice(os.listdir(voice_skin_dir))
        files = os.listdir(os.path.join(voice_skin_dir, voiceline))
        if files:
            files = [f for f in files if f.endswith('.ogg')]
            if files:
                print(os.path.join(voice_skin_dir, voiceline, rd.choice(files)))
                return os.path.join(voice_skin_dir, voiceline, rd.choice(files))
        return None


