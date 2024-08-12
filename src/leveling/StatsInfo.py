class StatsInfo:
    def __init__(self) -> None:
        pass

    def get_all_roles_id(self) -> list[int]:
        return [stat['id_role'] for stat in self.__stats.values()]

    def get_index_by_points(self, points: int) -> int:
        for x in self.__stats:
            if x == (len(self.__stats) - 1) or points < self.__stats[x + 1]['points']:
                return x

    def get_role_by_index(self, index: int) -> int:
        return self.__stats[index]['id_role']

    def get_points_by_index(self, index: int) -> int:
        return self.__stats[index]['points']

    __stats = {
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

STATS = {
    0: None,
    100: 1099149090744451073,
    200: 1099149715964174416,
    300: 1099149782930423898,
    400: 1099149889428017172,
    500: 1099149965697232967,
    620: 1099844523015798904,
    740: 1099844779044524103,
    860: 1099844840780472404,
    980: 1099844909747421274,
    1100: 1099844958686560256,
    1240: 1099845211452092456,
    1380: 1099845258638000199,
    1520: 1099845304125243483,
    1660: 1099845439404130385,
    1800: 1099845486254510250,
    1960: 1099845491409297408,
    2120: 1099845992569897051,
    2280: 1099846055350243369,
    2440: 1099846117811830924,
    2600: 1099846162506322010,
    2780: 1099847219311554620,
    2960: 1099847470630047816,
    3140: 1099847531715891291,
    3320: 1099847572794908692,
    3500: 1099847620983263262,
    3700: 1099847997166194792,
    4000: 1099848295909707818
}
