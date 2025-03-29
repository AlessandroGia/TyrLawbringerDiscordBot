import random
import yaml
import os

class Gifs:
    def __init__(self) -> None:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "quotes.yaml")
        with open(file_path, "r", encoding="utf-8") as file:
            self.gifs = yaml.safe_load(file)

    def get_random(self, category: str) -> str:
        if category in self.gifs:
            return random.choice(self.gifs[category])
        return "NaN"
