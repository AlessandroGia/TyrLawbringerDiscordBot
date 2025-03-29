import random
import yaml
import os

class Quotes:
    def __init__(self) -> None:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "quotes.yaml")
        with open(file_path, "r", encoding="utf-8") as file:
            self.quotes = yaml.safe_load(file)

    def get_random(self, category: str) -> str:
        if category in self.quotes:
            return random.choice(self.quotes[category])
        return "NaN"
