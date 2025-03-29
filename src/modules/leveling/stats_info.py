from config import Config

config = Config()

STATS = {
    0: None,
    100: int(config.get('ranks.bronze_5')),
    200: int(config.get('ranks.bronze_4')),
    300: int(config.get('ranks.bronze_3')),
    400: int(config.get('ranks.bronze_2')),
    500: int(config.get('ranks.bronze_1')),
    620: int(config.get('ranks.silver_5')),
    740: int(config.get('ranks.silver_4')),
    860: int(config.get('ranks.silver_3')),
    980: int(config.get('ranks.silver_2')),
    1100: int(config.get('ranks.silver_1')),
    1240: int(config.get('ranks.gold_5')),
    1380: int(config.get('ranks.gold_4')),
    1520: int(config.get('ranks.gold_3')),
    1660: int(config.get('ranks.gold_2')),
    1800: int(config.get('ranks.gold_1')),
    1960: int(config.get('ranks.platinum_5')),
    2120: int(config.get('ranks.platinum_4')),
    2280: int(config.get('ranks.platinum_3')),
    2440: int(config.get('ranks.platinum_2')),
    2600: int(config.get('ranks.platinum_1')),
    2780: int(config.get('ranks.diamond_5')),
    2960: int(config.get('ranks.diamond_4')),
    3140: int(config.get('ranks.diamond_3')),
    3320: int(config.get('ranks.diamond_2')),
    3500: int(config.get('ranks.diamond_1')),
    3700: int(config.get('ranks.master')),
    4000: int(config.get('ranks.grandmaster'))
}
