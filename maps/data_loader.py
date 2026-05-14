import csv
import math
import re
from collections import defaultdict
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"

BUILDING_NAMES = {
    "62": "John Hines",
    "63": "Building 63",
    "67": "Building 67",
}

B62_POSITIONS = {
    "1": {
        "195": (45.6, 35.4, 3.5, 4.8), "101": (45.0, 46.0, 5.0, 13.5),
        "196": (45.0, 59.5, 5.0, 5.4), "102": (47.2, 66.0, 3.6, 6.8),
        "106": (53.0, 49.0, 20.5, 12.2), "199": (55.8, 62.0, 7.0, 6.2),
        "105": (75.0, 49.0, 9.0, 12.2), "104": (85.0, 49.0, 8.5, 12.2),
        "104A": (82.0, 38.0, 6.0, 5.8), "197": (94.0, 50.0, 5.8, 16.0),
        "103": (96.0, 34.0, 3.5, 18.0),
    },
    "2": {
        "209B": (6.0, 22.0, 6.0, 18.0), "209C": (6.0, 41.0, 4.8, 6.5),
        "209": (15.0, 21.0, 24.0, 22.0), "209D": (39.5, 24.0, 4.6, 12.0),
        "218A": (44.6, 26.0, 5.8, 11.5), "218": (44.0, 38.5, 6.4, 13.0),

        "298": (0.5, 43.0, 5.0, 9.0), "217": (0.5, 67.0, 5.2, 9.5),
        "215": (6.0, 55.0, 6.0, 13.0), "214": (12.0, 55.0, 6.0, 13.0),
        "213": (18.0, 55.0, 6.0, 13.0), "212": (24.0, 55.0, 6.0, 13.0),
        "211": (30.0, 55.0, 6.0, 13.0), "210": (36.0, 55.0, 6.0, 13.0),
        "208": (42.0, 55.0, 6.0, 13.0), "207": (48.0, 55.0, 5.0, 12.0),

        "206": (44.5, 68.0, 9.8, 8.0), "205": (53.6, 76.8, 2.8, 3.0),
        "204": (45.0, 80.0, 9.5, 8.5), "203": (56.5, 80.0, 14.5, 8.5),
        "296": (51.2, 50.6, 3.0, 4.0), "297": (55.7, 69.8, 5.0, 6.8),

        "220A": (51.0, 12.0, 5.5, 9.5), "220B": (56.5, 8.0, 6.0, 12.0),
        "221A": (62.5, 8.0, 6.5, 12.0), "221B": (69.0, 8.0, 6.5, 12.0),
        "221C": (75.5, 8.0, 6.5, 12.0), "221D": (82.0, 8.0, 6.5, 12.0),
        "220": (51.0, 27.4, 9.0, 5.8), "295": (58.0, 20.0, 6.0, 6.6),
        "294": (64.0, 21.0, 18.0, 7.0), "219": (50.5, 36.0, 9.0, 12.6),
        "221": (60.5, 34.0, 21.5, 15.0), "240": (55.2, 49.6, 4.2, 3.0),
        "293": (62.2, 50.2, 16.0, 3.4),

        "222": (96.0, 27.0, 3.0, 14.0), "223E": (88.0, 24.0, 3.8, 13.0),
        "223F": (92.2, 24.0, 3.4, 14.0), "222B": (88.1, 37.0, 3.8, 4.0),
        "222A": (88.1, 42.2, 3.8, 3.8), "226": (94.6, 43.0, 4.4, 14.0),
        "292": (89.3, 49.0, 4.8, 5.0), "223A": (83.2, 45.7, 4.6, 9.0),
        "228": (89.5, 58.0, 9.0, 11.0), "229": (82.8, 56.2, 6.4, 12.6),
        "230": (76.4, 56.2, 5.7, 12.6), "231": (70.1, 56.2, 5.4, 12.6),
        "232": (65.2, 56.2, 4.0, 12.6), "233": (58.6, 55.2, 4.8, 5.6),
        "233A": (58.6, 62.2, 6.2, 6.0), "234": (54.8, 56.4, 3.0, 11.4),
        "299": (64.9, 69.8, 6.8, 6.9),
    },
    "3": {
        "398": (0.5, 43.0, 4.2, 8.5), "318": (0.8, 65.0, 4.4, 8.0),
        "316": (6.0, 54.0, 5.6, 13.0), "315": (12.0, 54.0, 5.6, 13.0),
        "314": (18.0, 54.0, 5.6, 13.0), "313": (24.0, 54.0, 5.6, 13.0),
        "312": (30.0, 54.0, 5.6, 13.0), "311": (36.0, 54.0, 5.6, 13.0),
        "310": (42.0, 54.0, 5.6, 13.0), "309": (48.0, 53.6, 4.5, 8.8),
        "306": (42.8, 68.8, 10.0, 8.0), "305": (53.0, 77.4, 3.0, 3.0),
        "304": (43.0, 80.0, 10.0, 8.0), "303": (57.0, 82.0, 8.0, 6.0),
        "303A": (65.0, 82.0, 8.0, 6.0), "395": (54.2, 80.8, 2.6, 4.0),

        "319": (6.0, 20.0, 27.0, 20.0), "320": (36.0, 20.0, 6.0, 14.0),
        "321": (43.0, 20.0, 6.0, 14.0), "324": (50.0, 18.0, 10.0, 17.0),
        "324A": (60.3, 12.0, 3.5, 5.0), "326": (60.3, 18.0, 4.7, 12.0),
        "326A": (65.5, 18.0, 6.0, 17.0), "327": (72.0, 18.0, 6.0, 16.0),
        "328": (79.0, 20.0, 13.0, 17.0), "329": (94.0, 20.0, 4.2, 14.0),

        "319A": (40.0, 40.0, 5.0, 6.0), "396": (50.0, 39.0, 7.0, 8.0),
        "307": (53.2, 48.5, 2.4, 3.6), "337": (54.2, 53.0, 2.2, 3.6),
        "338": (54.2, 57.4, 2.2, 4.0), "397": (55.0, 68.8, 5.2, 8.4),
        "399": (61.2, 69.0, 6.8, 7.0),

        "336": (56.8, 54.0, 5.8, 13.0), "335": (63.2, 54.0, 5.8, 13.0),
        "334": (69.6, 54.0, 5.8, 13.0), "333": (76.0, 54.0, 8.8, 13.0),
        "332A": (84.3, 45.0, 2.8, 4.5), "332": (85.2, 54.0, 5.0, 13.0),
        "331": (90.6, 54.0, 4.4, 13.0), "330": (95.4, 54.0, 3.8, 13.0),
    },
    "4": {
        "398": (0.5, 43.0, 4.2, 8.5), "414": (0.8, 66.0, 4.4, 8.5),
        "415": (6.0, 18.0, 4.8, 12.0), "412": (10.8, 20.0, 19.5, 20.0),
        "416": (31.0, 18.0, 5.0, 13.0), "417A": (36.5, 18.0, 5.0, 6.0),
        "417B": (42.0, 18.0, 5.0, 6.0), "417C": (39.4, 25.0, 7.6, 5.7),
        "417D": (39.4, 31.8, 7.6, 6.0),

        "418": (48.5, 18.0, 8.0, 20.0), "419": (57.5, 18.0, 5.2, 20.0),
        "420": (63.5, 18.0, 5.2, 20.0), "421": (69.5, 18.0, 5.6, 20.0),
        "422": (76.0, 18.0, 5.0, 20.0), "424": (82.0, 20.0, 15.0, 20.0),

        "411": (22.0, 55.0, 5.5, 13.0), "410A": (28.5, 55.0, 5.7, 13.0),
        "410": (35.0, 55.0, 13.0, 13.0), "408": (49.0, 55.0, 6.0, 13.0),
        "406": (42.8, 68.8, 10.0, 8.0), "405": (53.0, 77.4, 3.0, 3.0),
        "404": (43.0, 80.0, 10.0, 8.0), "403": (57.0, 82.0, 14.0, 6.0),

        "494": (44.5, 44.0, 3.8, 4.6), "440": (59.0, 43.0, 4.2, 5.0),
        "407": (53.5, 50.0, 2.8, 3.6), "496": (56.8, 58.5, 5.0, 8.5),
        "434": (62.3, 52.0, 2.8, 3.8), "435": (62.3, 60.0, 2.8, 4.2),
        "497": (56.8, 69.8, 5.0, 6.8), "499": (65.0, 69.8, 6.8, 6.9),

        "433A": (69.0, 53.0, 5.4, 8.0), "433": (68.0, 62.0, 8.0, 7.0),
        "431": (77.2, 53.0, 2.8, 4.5), "424A": (80.4, 53.0, 2.5, 5.0),
        "432": (78.8, 59.0, 5.5, 10.0), "429": (86.0, 55.0, 4.5, 13.0),
        "428": (91.0, 55.0, 4.2, 13.0), "427": (95.6, 55.0, 3.6, 13.0),
        "495": (76.0, 44.0, 3.8, 4.6), "498": (0.5, 49.5, 4.2, 5.5),
    },
    "5": {
        "598": (0.5, 43.0, 4.2, 8.5), "516": (0.8, 66.0, 4.4, 8.5),
        "514": (6.0, 18.0, 5.4, 20.0), "512": (12.0, 18.0, 18.0, 20.0),
        "517B": (31.0, 18.0, 5.4, 6.5), "517A": (36.8, 18.0, 5.4, 6.5),
        "517": (31.0, 25.6, 11.4, 12.4), "519A": (43.0, 18.0, 6.0, 8.0),
        "519B": (43.0, 27.0, 6.0, 10.5), "519": (50.5, 19.0, 10.8, 18.8),
        "522": (62.8, 19.0, 5.5, 11.5), "595": (62.8, 31.0, 3.4, 3.5),
        "522A": (63.0, 35.0, 3.6, 4.2), "523A": (69.0, 19.0, 5.6, 12.0),
        "523": (75.0, 20.0, 8.0, 18.0), "526A": (83.8, 18.0, 4.6, 9.5),
        "526": (83.8, 28.5, 4.6, 11.0), "527A": (89.0, 18.0, 4.8, 11.0),
        "527": (89.0, 30.0, 4.8, 9.5), "528": (94.4, 20.0, 4.8, 18.8),

        "511": (6.0, 55.0, 5.7, 13.0), "510": (12.5, 55.0, 6.0, 13.0),
        "509": (19.0, 55.0, 6.0, 13.0), "507A": (31.0, 53.0, 10.0, 6.4),
        "507B": (31.0, 60.5, 10.0, 7.2), "507": (42.0, 55.0, 10.0, 13.0),
        "507C": (52.5, 52.5, 3.0, 3.8), "508": (56.0, 51.8, 3.0, 3.8),
        "596": (58.6, 45.0, 4.6, 6.0), "536": (62.8, 56.0, 2.8, 4.0),
        "537": (62.8, 61.2, 3.0, 4.0), "597": (56.8, 69.8, 5.0, 6.8),
        "599": (65.0, 69.8, 6.8, 6.9),

        "535": (67.5, 54.0, 6.5, 14.0), "534": (75.0, 54.0, 8.0, 14.0),
        "533": (84.0, 54.0, 7.0, 14.0), "532": (91.8, 55.0, 3.4, 13.0),
        "531": (95.8, 55.0, 3.2, 13.0),

        "506": (42.8, 68.8, 10.0, 8.0), "505": (53.0, 77.4, 3.0, 3.0),
        "504": (43.0, 80.0, 10.0, 8.0), "503": (57.0, 82.0, 8.0, 6.0),
        "503A": (65.0, 82.0, 8.0, 6.0), "593": (82.0, 43.4, 10.5, 4.5),
        "594": (38.0, 41.5, 3.0, 3.4),
    },
    "6": {
        "698": (0.5, 43.0, 4.2, 13.5), "612": (6.0, 52.0, 6.2, 16.0),
        "613": (6.0, 18.0, 6.2, 20.0), "614": (13.0, 18.0, 9.0, 18.0),
        "615": (22.8, 18.0, 9.0, 18.0), "617": (32.6, 18.0, 9.0, 18.0),
        "696": (13.0, 39.0, 28.5, 5.0), "610": (19.0, 47.0, 7.0, 5.5),
        "611": (13.0, 54.0, 10.5, 14.0), "609": (24.0, 54.0, 11.0, 14.0),
        "608": (36.0, 51.0, 6.0, 17.0),

        "618": (42.0, 18.0, 31.0, 30.0), "697": (50.0, 48.5, 14.0, 12.0),
        "606": (42.2, 57.5, 16.0, 11.0), "607": (53.0, 49.5, 3.0, 4.4),
        "605": (42.5, 70.5, 5.4, 6.8), "604": (48.5, 72.0, 5.4, 6.5),
        "603": (55.0, 71.5, 5.0, 8.0), "601": (61.5, 80.0, 7.0, 5.8),
        "602": (69.0, 80.0, 10.5, 5.8),

        "619": (74.0, 18.0, 10.5, 18.0), "620": (85.0, 18.0, 6.4, 18.0),
        "621": (92.0, 18.0, 7.0, 22.0), "695": (76.0, 42.5, 21.0, 6.0),
        "624": (78.0, 49.5, 6.0, 6.0), "623": (84.0, 54.0, 9.5, 14.0),
        "622": (94.5, 53.0, 4.5, 16.0), "625": (76.0, 58.0, 7.0, 10.5),
        "626": (69.2, 54.0, 6.2, 14.0), "627": (63.0, 55.0, 5.2, 13.0),
        "628": (58.8, 55.0, 3.6, 13.0), "699": (65.0, 69.8, 6.8, 6.9),
        "JH-6-190": (38.5, 78.5, 5.0, 5.0),
    },
}

B62_FLOOR_META = {
    "1": {
        "aspect_ratio": "1.78 / 1",
        "map_zoom": "1",
        "outline_points": "1,42 4.8,42 4.8,25 7.2,25 7.2,8 9.2,8 9.2,25 14.5,25 14.5,8 16.5,8 16.5,25 24.0,25 24.0,8 26.0,8 26.0,25 34.0,25 34.0,8 36.0,8 36.0,25 46.5,25 46.5,4.5 77.5,4.5 77.5,25 98.0,25 98.0,45 100,45 100,58 96.0,58 96.0,66 92.0,66 92.0,55 87.0,55 87.0,61.5 73.5,61.5 73.5,68 64.0,68 64.0,73 50.0,73 50.0,65 45.0,65 45.0,50 1,50",
        "corridors": [
            {"x": 3.0, "y": 39.0, "w": 91.5, "h": 5.0},
            {"x": 48.8, "y": 44.0, "w": 3.6, "h": 29.0},
            {"x": 52.0, "y": 59.0, "w": 15.0, "h": 5.5},
            {"x": 67.0, "y": 44.0, "w": 28.0, "h": 5.2},
            {"x": 52.0, "y": 67.5, "w": 14.0, "h": 7.0},
        ],
        "walls": [
            {"x1": 45.0, "y1": 44.0, "x2": 45.0, "y2": 65.0},
            {"x1": 50.0, "y1": 44.0, "x2": 50.0, "y2": 73.0},
            {"x1": 52.0, "y1": 61.3, "x2": 67.0, "y2": 61.3},
            {"x1": 52.0, "y1": 67.5, "x2": 66.0, "y2": 67.5},
            {"x1": 66.0, "y1": 59.0, "x2": 66.0, "y2": 74.5},
            {"x1": 73.5, "y1": 44.0, "x2": 73.5, "y2": 61.2},
            {"x1": 84.0, "y1": 44.0, "x2": 84.0, "y2": 61.2},
            {"x1": 93.5, "y1": 44.0, "x2": 93.5, "y2": 66.0},
        ],
        "entrance_x": 47.7, "entrance_y": 84,
    },
    "2": {
        "aspect_ratio": "2.22 / 1",
        "outline_points": "0,38 5,38 5,12 35,12 35,7 49,7 49,0 77,0 77,8 99,8 99,62 96,62 96,74 70,74 70,91 43,91 43,78 35,78 35,68 0,68",
        "corridors": [
            {"x": 5, "y": 43, "w": 87, "h": 7},
            {"x": 42, "y": 42, "w": 6, "h": 37},
            {"x": 54, "y": 27, "w": 35, "h": 6},
            {"x": 50, "y": 50, "w": 38, "h": 6},
            {"x": 55, "y": 68, "w": 15, "h": 7},
        ],
        "walls": [
            {"x1": 5.0, "y1": 43.0, "x2": 92.0, "y2": 43.0},
            {"x1": 5.0, "y1": 50.0, "x2": 92.0, "y2": 50.0},
            {"x1": 42.0, "y1": 42.0, "x2": 42.0, "y2": 79.0},
            {"x1": 48.0, "y1": 42.0, "x2": 48.0, "y2": 79.0},
            {"x1": 60.0, "y1": 27.0, "x2": 89.0, "y2": 27.0},
            {"x1": 60.0, "y1": 33.0, "x2": 89.0, "y2": 33.0},
            {"x1": 60.0, "y1": 50.0, "x2": 88.0, "y2": 50.0},
            {"x1": 60.0, "y1": 56.0, "x2": 88.0, "y2": 56.0},
        ],
        "entrance_x": 44, "entrance_y": 90,
    },
    "3": {
        "aspect_ratio": "2.22 / 1",
        "outline_points": "0,38 5,38 5,12 36,12 36,8 49,8 49,0 77,0 77,8 97,8 97,62 94,62 94,74 68,74 68,91 42,91 42,78 35,78 35,68 0,68",
        "corridors": [
            {"x": 5, "y": 42, "w": 88, "h": 8}, {"x": 42, "y": 40, "w": 6, "h": 37},
            {"x": 56, "y": 35, "w": 34, "h": 8}, {"x": 48, "y": 50, "w": 40, "h": 6},
            {"x": 55, "y": 68, "w": 14, "h": 7},
        ],
        "entrance_x": 44, "entrance_y": 90,
    },
    "4": {
        "aspect_ratio": "2.22 / 1",
        "outline_points": "0,38 5,38 5,12 36,12 36,8 49,8 49,0 77,0 77,8 97,8 97,62 94,62 94,74 68,74 68,91 42,91 42,78 35,78 35,68 0,68",
        "corridors": [
            {"x": 5, "y": 42, "w": 88, "h": 8},
            {"x": 42, "y": 40, "w": 6, "h": 37},
            {"x": 48, "y": 50, "w": 40, "h": 6},
            {"x": 55, "y": 68, "w": 14, "h": 7},
            {"x": 55, "y": 38, "w": 26, "h": 5},
        ],
        "entrance_x": 44,
        "entrance_y": 90,
    },
    "5": {
        "aspect_ratio": "2.22 / 1",
        "outline_points": "0,38 5,38 5,12 36,12 36,8 49,8 49,0 77,0 77,8 97,8 97,62 94,62 94,74 68,74 68,91 42,91 42,78 35,78 35,68 0,68",
        "corridors": [
            {"x": 5, "y": 42, "w": 88, "h": 8},
            {"x": 42, "y": 40, "w": 6, "h": 37},
            {"x": 48, "y": 50, "w": 40, "h": 6},
            {"x": 55, "y": 68, "w": 14, "h": 7},
            {"x": 58, "y": 38, "w": 31, "h": 5},
        ],
        "entrance_x": 44,
        "entrance_y": 90,
    },
    "6": {
        "aspect_ratio": "2.22 / 1",
        "outline_points": "0,38 5,38 5,12 36,12 36,8 42,8 42,0 74,0 74,8 98,8 98,40 100,40 100,68 96,68 96,75 69,75 69,91 41,91 41,75 36,75 36,68 0,68",
        "corridors": [
            {"x": 5, "y": 40, "w": 92, "h": 7},
            {"x": 42, "y": 47, "w": 36, "h": 8},
            {"x": 42, "y": 55, "w": 6, "h": 24},
            {"x": 58, "y": 68, "w": 15, "h": 7},
            {"x": 76, "y": 47, "w": 21, "h": 7},
        ],
        "entrance_x": 44,
        "entrance_y": 90,
    },
}


def _room_code(label, fallback):
    label = (label or "").strip()
    if " - " in label:
        return label.split(" - ", 1)[0].strip()
    match = re.match(r"([A-Za-z]*\d+[A-Za-z]*)", label)
    return match.group(1) if match else fallback


def _room_name(label, code):
    label = (label or "").strip()
    if " - " in label:
        return label.split(" - ", 1)[1].strip()
    if label and label != code:
        return label
    return f"Room {code}"


def _clean_building_number(building):
    match = re.search(r"Building\s*(\d+)|\b(\d+)\b", building or "")
    return (match.group(1) or match.group(2)) if match else (building or "").strip()


def _display_building_name(number, building_label):
    if number in BUILDING_NAMES:
        return BUILDING_NAMES[number]
    return re.sub(r"\s*\(Building\s*\d+\)\s*", "", building_label or "").strip() or f"Building {number}"


def _room_type(row_type):
    value = (row_type or "").strip()
    if not value:
        return "room"
    return value.replace("_", " ").title()


def _make_room(row, index):
    code = _room_code(row.get("label"), row.get("id", f"room-{index}"))
    name = _room_name(row.get("label"), code)
    room_type = _room_type(row.get("type"))
    return {
        "code": code,
        "name": name,
        "type": room_type,
        "area": "",
        "source_id": row.get("id", ""),
        "lat": row.get("lat"),
        "lng": row.get("lng"),
        "x": 8,
        "y": 18,
        "w": 8,
        "h": 7,
        "route_points": "",
        "summary": f"{code} is listed as {name} in the data file.",
        "steps": [
            "Select the matching room from the loaded data.",
            "Use the floor shown on this page.",
            f"Look for the room sign labelled {code}.",
        ],
    }


def _position_rooms(rooms):
    count = len(rooms)
    if not count:
        return

    columns = min(9, max(3, math.ceil(math.sqrt(count * 1.35))))
    rows = math.ceil(count / columns)
    cell_w = 84 / columns
    cell_h = 62 / rows
    room_w = min(9.5, max(5.2, cell_w * 0.72))
    room_h = min(8.0, max(4.8, cell_h * 0.66))

    rooms.sort(key=lambda room: (room["code"].zfill(8), room["name"]))
    for index, room in enumerate(rooms):
        row = index // columns
        col = index % columns
        x = 8 + (col * cell_w) + ((cell_w - room_w) / 2)
        y = 18 + (row * cell_h) + ((cell_h - room_h) / 2)
        room["x"] = round(x, 2)
        room["y"] = round(y, 2)
        room["w"] = round(room_w, 2)
        room["h"] = round(room_h, 2)
        cx = room["x"] + (room["w"] / 2)
        cy = room["y"] + (room["h"] / 2)
        room["route_points"] = f"10,82 18,82 18,{cy:.1f} {cx:.1f},{cy:.1f}"


def _make_floor(level, rooms, building_number=None):
    _position_rooms(rooms)
    floor = {
        "level": str(level),
        "label": f"Level {level}",
        "outline_points": "6,12 94,12 94,88 6,88",
        "entrance_x": 10,
        "entrance_y": 82,
        "corridors": [
            {"x": 10, "y": 78, "w": 80, "h": 6},
            {"x": 16, "y": 18, "w": 6, "h": 66},
            {"x": 16, "y": 48, "w": 72, "h": 6},
        ],
        "walls": [
            {"x1": 6, "y1": 12, "x2": 94, "y2": 12},
            {"x1": 94, "y1": 12, "x2": 94, "y2": 88},
            {"x1": 94, "y1": 88, "x2": 6, "y2": 88},
            {"x1": 6, "y1": 88, "x2": 6, "y2": 12},
        ],
        "labels": [
            {"text": "rooms from data file", "x": 50, "y": 10},
            {"text": "main path", "x": 50, "y": 76},
        ],
        "rooms": rooms,
    }

    if building_number == "62" and str(level) in B62_FLOOR_META:
        _apply_b62_layout(floor)
    return floor


def _apply_b62_layout(floor):
    level = floor["level"]
    meta = B62_FLOOR_META[level]
    floor.update({
        "real_layout": True,
        "aspect_ratio": meta.get("aspect_ratio", "2.42 / 1"),
        "map_zoom": meta.get("map_zoom", "1"),
        "outline_points": meta["outline_points"],
        "corridors": meta["corridors"],
        "walls": meta.get("walls", []),
        "labels": [],
        "entrance_x": meta["entrance_x"],
        "entrance_y": meta["entrance_y"],
    })
    positions = B62_POSITIONS[level]
    for room in floor["rooms"]:
        position = positions.get(room["code"])
        if not position:
            continue
        room["x"], room["y"], room["w"], room["h"] = position
        cx = room["x"] + (room["w"] / 2)
        cy = room["y"] + (room["h"] / 2)
        room["route_points"] = f"{floor['entrance_x']},{floor['entrance_y']} 45,75 45,47 {cx:.1f},{cy:.1f}"


def _building_from_rows(number, building_label, rows, source_name):
    floors = defaultdict(dict)
    for index, row in enumerate(rows):
        floor = str(row.get("floor", "")).strip() or "Unknown"
        room = _make_room(row, index)
        floors[floor].setdefault(room["code"], room)

    ordered_floors = []
    for level, room_map in sorted(floors.items(), key=lambda item: _floor_sort_key(item[0])):
        floor = _make_floor(level, list(room_map.values()), number)
        ordered_floors.append(floor)
    name = _display_building_name(number, building_label)

    return {
        "id": number,
        "number": number,
        "name": name,
        "campus": "St Lucia",
        "description": f"Loaded from data/{source_name}.",
        "floors": ordered_floors,
    }


def _floor_sort_key(level):
    match = re.match(r"(\d+)(.*)", str(level))
    if not match:
        return (999, str(level))
    return (int(match.group(1)), match.group(2))


def _read_node_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "id" not in reader.fieldnames or "label" not in reader.fieldnames:
            return None
        rows = [row for row in reader if row.get("id") and row.get("label")]

    if not rows:
        return None

    building_label = rows[0].get("building", "")
    number = _clean_building_number(building_label)
    return _building_from_rows(number, building_label, rows, path.name)


def _read_building_67(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.lower().startswith("| id "):
            continue

        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 8:
            continue

        identifier = parts[7].replace("identifier=", "").strip()
        rows.append({
            "id": f"67-{parts[0]}-{identifier[:8]}",
            "building": parts[1],
            "floor": parts[2],
            "type": parts[3],
            "label": parts[0],
            "lat": parts[5].replace("lat=", "").strip(),
            "lng": parts[6].replace("lng=", "").strip(),
            "uq_maps_identifier": identifier,
        })

    return _building_from_rows("67", "67", rows, path.name) if rows else None


def load_buildings_from_data_folder():
    buildings = []

    for path in sorted(DATA_DIR.glob("*.csv")):
        building = _read_node_csv(path)
        if building:
            buildings.append(building)

    building_67 = DATA_DIR / "building_67.txt"
    if building_67.exists():
        building = _read_building_67(building_67)
        if building:
            buildings.append(building)

    buildings.sort(key=lambda building: int(building["number"]) if building["number"].isdigit() else 999)
    return buildings
