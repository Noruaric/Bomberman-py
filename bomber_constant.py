"""represent all the bomberman constant"""
from pygame import mixer

# DEBUG
DEBUG_SHOW_BOMBER_PLACEMENT = True
DEBUG_FULLSCREEN = False
DEBUG_FAST_HURRY = False
DEBUG_USE_SAME_BLAST = True

# Clasic Power up
BLAST_PLUS = "blast+"
SPEED_PLUS = "speed+"
BOMB_PLUS = "bomb+"

# Clasic Power down
BLAST_MINUS = "blast-"
SPEED_MINUS = "speed-"
BOMB_MINUS = "bomb-"

# Item
HEART_ITEM = "heart item"
POWER_GLOVE_ITEM = "power glove item"
KICK_ITEM = "kick item"
FOOTKICK_ITEM = "footkick item"
SPIKE_BOMB_ITEM = "spikebombs"

# SPECIAL
SKULL_DISEAS = "crane diseas"
MAX_BOMB_POWER = "max blast"
EGG = "EGG OBJ"

# INDEX
POWER_GLOVE_INDEX = 0
FOOTKICK_INDEX = 1
KICK_INDEX = 2
SPIKE_BOMB_INDEX = 3


ALL_ITEM_POWER_UP = [
    BLAST_PLUS,
    SPEED_PLUS,
    BOMB_PLUS,
    BLAST_MINUS,
    SPEED_MINUS,
    BOMB_MINUS,
    HEART_ITEM,
    POWER_GLOVE_ITEM,
    KICK_ITEM,
    FOOTKICK_ITEM,
    SPIKE_BOMB_ITEM,
    SKULL_DISEAS,
    MAX_BOMB_POWER,
    EGG,
]

# other
EMPTY_CASE = "nothinghere"

EXPLOSED_BLOCK = "ebc"
BLAST_CENTER = "BlastC"
BLAST_LEFT = "BlastL"
BLAST_RIGHT = "BlastR"
BLAST_UP = "BlastU"
BLAST_DOWN = "BlastD"
BLAST_LEFTMAX = "BlastLMAX"
BLAST_RIGHTMAX = "BlastRMAX"
BLAST_UPMAX = "BlastUMAX"
BLAST_DOWNMAX = "BlastDMAX"

EXPLOSED_BLOCK_BY_SPIKEBOMB = "ebcSPIKE"
BLAST_CENTER_SPIKEBOMB = "BlastCSPIKE"
BLAST_LEFT_SPIKEBOMB = "BlastLSPIKE"
BLAST_RIGHT_SPIKEBOMB = "BlastRSPIKE"
BLAST_UP_SPIKEBOMB = "BlastUSPIKE"
BLAST_DOWN_SPIKEBOMB = "BlastDSPIKE"
BLAST_LEFTMAX_SPIKEBOMB = "BlastLMAXSPIKE"
BLAST_RIGHTMAX_SPIKEBOMB = "BlastRMAXSPIKE"
BLAST_UPMAX_SPIKEBOMB = "BlastUMAXSPIKE"
BLAST_DOWNMAX_SPIKEBOMB = "BlastDMAXSPIKE"

EVRY_EXPLOSION_TYPE = [
    EXPLOSED_BLOCK,
    BLAST_CENTER,
    BLAST_LEFT,
    BLAST_RIGHT,
    BLAST_UP,
    BLAST_DOWN,
    BLAST_LEFTMAX,
    BLAST_RIGHTMAX,
    BLAST_UPMAX,
    BLAST_DOWNMAX,
    EXPLOSED_BLOCK_BY_SPIKEBOMB,
    BLAST_CENTER_SPIKEBOMB,
    BLAST_LEFT_SPIKEBOMB,
    BLAST_RIGHT_SPIKEBOMB,
    BLAST_UP_SPIKEBOMB,
    BLAST_DOWN_SPIKEBOMB,
    BLAST_LEFTMAX_SPIKEBOMB,
    BLAST_RIGHTMAX_SPIKEBOMB,
    BLAST_UPMAX_SPIKEBOMB,
    BLAST_DOWNMAX_SPIKEBOMB,
]


def arena_temp():
    arena_template = [
        [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
        [3, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 3],
        [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
    ]
    for i in range(9):
        for y in range(13):
            if arena_template[i][y] == 3:
                arena_template[i][y] = EMPTY_CASE
            elif arena_template[i][y] == 0:
                arena_template[i][y] = EMPTY_DESTRUCTIBLE
            elif arena_template[i][y] == 1:
                arena_template[i][y] = INDESTRUCTIBLE_BLOCK
    return arena_template


# BLOCKS
EMPTY_DESTRUCTIBLE = "BC0"
BLOCK_BLAST_PLUS = "BC1"
BLOCK_SPEED_PLUS = "BC2"
BLOCK_BOMB_PLUS = "BC3"
BLOCK_BLAST_MINUS = "BC4"
BLOCK_SPEED_MINUS = "BC5"
BLOCK_BOMB_MINUS = "BC6"
BLOCK_HEART = "BC7"
BLOCK_POWER_GLOVE = "BC8"
BLOCK_KICK = "BC9"
BLOCK_FOOTKICK = "BC10"
BLOCK_SPIKE_BOMB = "BC11"
BLOCK_SKULL_DISEAS = "BC12"
BLOCK_MAX_BOMB_POWER = "BC13"
INDESTRUCTIBLE_BLOCK = "IBC"
LETHAL_BLOCK = "PBC"  # also know as pressure block

POWER_UP_BLOCKS = [
    BLOCK_BLAST_PLUS,
    BLOCK_SPEED_PLUS,
    BLOCK_BOMB_PLUS,
    BLOCK_BLAST_MINUS,
    BLOCK_SPEED_MINUS,
    BLOCK_BOMB_MINUS,
    # BLOCK_POWER_GLOVE,
    # BLOCK_KICK,
    # BLOCK_FOOTKICK,
    BLOCK_SPIKE_BOMB,
    # BLOCK_SKULL_DISEAS,
    BLOCK_MAX_BOMB_POWER,
]

BLOCK_TO_POWER_UP = {
    BLOCK_BLAST_PLUS: BLAST_PLUS,
    BLOCK_SPEED_PLUS: SPEED_PLUS,
    BLOCK_BOMB_PLUS: BOMB_PLUS,
    BLOCK_BLAST_MINUS: BLAST_MINUS,
    BLOCK_SPEED_MINUS: SPEED_MINUS,
    BLOCK_BOMB_MINUS: BOMB_MINUS,
    BLOCK_POWER_GLOVE: POWER_GLOVE_ITEM,
    BLOCK_KICK: KICK_ITEM,
    BLOCK_FOOTKICK: FOOTKICK_ITEM,
    BLOCK_SPIKE_BOMB: SPIKE_BOMB_ITEM,
    BLOCK_SKULL_DISEAS: SKULL_DISEAS,
    BLOCK_MAX_BOMB_POWER: MAX_BOMB_POWER,
}

ALL_DESTRUCTIBLE_BLOCK = [
    EMPTY_DESTRUCTIBLE,
    BLOCK_BLAST_PLUS,
    BLOCK_SPEED_PLUS,
    BLOCK_BOMB_PLUS,
    BLOCK_BLAST_MINUS,
    BLOCK_SPEED_MINUS,
    BLOCK_BOMB_MINUS,
    BLOCK_POWER_GLOVE,
    BLOCK_KICK,
    BLOCK_FOOTKICK,
    BLOCK_SPIKE_BOMB,
    BLOCK_SKULL_DISEAS,
    BLOCK_MAX_BOMB_POWER,
    BLOCK_HEART,
]

ALL_BLOCK = [
    LETHAL_BLOCK,
    EMPTY_DESTRUCTIBLE,
    BLOCK_BLAST_PLUS,
    BLOCK_SPEED_PLUS,
    BLOCK_BOMB_PLUS,
    BLOCK_BLAST_MINUS,
    BLOCK_SPEED_MINUS,
    BLOCK_BOMB_MINUS,
    BLOCK_POWER_GLOVE,
    BLOCK_KICK,
    BLOCK_FOOTKICK,
    BLOCK_SPIKE_BOMB,
    BLOCK_SKULL_DISEAS,
    BLOCK_MAX_BOMB_POWER,
    BLOCK_HEART,
    INDESTRUCTIBLE_BLOCK,
]

# MUSICS PATH (relatif)

MENU_MUSIC_START = "./musique/Main Menu Bomberman 2 DS (OST) start.mp3"  # from the game : "Bomberman 2"
MENU_MUSIC_LOOP = (
    "./musique/Main Menu Bomberman 2 DS (OST) loop.mp3"  # from the game : "Bomberman 2"
)
BATTLE_MUSIC = [
    "./musique/Battle Theme 1 Normal Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 2 Lost World Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 3 Ghost Town Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 4 Miner Cave Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 5 Techno Machines Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
]

BATTLE_MUSIC_HURY_UP = [
    "./musique/Battle Theme 1 Normal Hurry Up! Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 2 Lost World Hurry Up! Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 3 Ghost Town Hurry Up! Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 4 Miner Cave Hurry Up! Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
    "./musique/Battle Theme 5 Techno Machines Hurry Up! Bomberman 2 DS (OST).mp3",  # from the game : "Bomberman 2"
]

MUSIC_NAME_LIST = [
    "Battle Theme 1 Normal from Bomberman 2 DS",
    "Battle Theme 2 Lost World from Bomberman 2 DS",
    "Battle Theme 3 Ghost Town from Bomberman 2 DS",
    "Battle Theme 4 Miner Cave from Bomberman 2 DS",
    "Battle Theme 5 Techno Machines from Bomberman 2 DS",
]

PREPARING_FOR_BATTLE = ""  # from the game : ""


# Image Path (relatif)
PATH_ARENA_BG = "./graphisme/Bomber Arena.png"
PATH_DESTRUCTIBLE_BLOCKS = "./graphisme/Destructible_block.png"
PATH_LETHAL_BLOCKS = "./graphisme/lethal block.png"
BOMB1 = ""
BOMB2 = ""
BOMB3 = ""
BOMB1_SPIKES = ""
BOMB2_SPIKES = ""
BOMB3_SPIKES = ""


EXPLOSION_UP = [f"./graphisme/bomb & blast/up ({i}).png" for i in range(1, 5)]
EXPLOSION_DOWN = [f"./graphisme/bomb & blast/down ({i}).png" for i in range(1, 5)]
EXPLOSION_LEFT = [f"./graphisme/bomb & blast/left ({i}).png" for i in range(1, 5)]
EXPLOSION_RIGHT = [f"./graphisme/bomb & blast/right ({i}).png" for i in range(1, 5)]
EXPLOSION_CENTER = [f"./graphisme/bomb & blast/center ({i}).png" for i in range(1, 5)]
EXPLOSION_UP_MAX = [f"./graphisme/bomb & blast/upmax ({i}).png" for i in range(1, 5)]
EXPLOSION_DOWN_MAX = [
    f"./graphisme/bomb & blast/downmax ({i}).png" for i in range(1, 5)
]
EXPLOSION_LEFT_MAX = [
    f"./graphisme/bomb & blast/leftmax ({i}).png" for i in range(1, 5)
]
EXPLOSION_RIGHT_MAX = [
    f"./graphisme/bomb & blast/rightmax ({i}).png" for i in range(1, 5)
]
EXPLOSED_BLOCK_PATH = ["./graphisme/Destructible_block.png"] * 4

EXPLOSION_UP_BLUE = []
EXPLOSION_DOWN_BLUE = []
EXPLOSION_LEFT_BLUE = []
EXPLOSION_RIGHT_BLUE = []
EXPLOSION_CENTER_BLUE = []
EXPLOSION_UP_MAX_BLUE = []
EXPLOSION_DOWN_MAX_BLUE = []
EXPLOSION_LEFT_MAX_BLUE = []
EXPLOSION_RIGHT_MAX_BLUE = []
EXPLOSED_BLOCK_PATH_BLUE = []

if DEBUG_USE_SAME_BLAST:
    EXPLOSION_UP_BLUE = EXPLOSION_UP
    EXPLOSION_DOWN_BLUE = EXPLOSION_DOWN
    EXPLOSION_LEFT_BLUE = EXPLOSION_LEFT
    EXPLOSION_RIGHT_BLUE = EXPLOSION_RIGHT
    EXPLOSION_CENTER_BLUE = EXPLOSION_CENTER
    EXPLOSION_UP_MAX_BLUE = EXPLOSION_UP_MAX
    EXPLOSION_DOWN_MAX_BLUE = EXPLOSION_DOWN_MAX
    EXPLOSION_LEFT_MAX_BLUE = EXPLOSION_LEFT_MAX
    EXPLOSION_RIGHT_MAX_BLUE = EXPLOSION_RIGHT_MAX
    EXPLOSED_BLOCK_PATH_BLUE = EXPLOSED_BLOCK_PATH

ONFLOOR_BLAST_PLUS = "./graphisme/items/flame.png"
ONFLOOR_SPEED_PLUS = "./graphisme/items/patin.png"
ONFLOOR_BOMB_PLUS = "./graphisme/items/bomb plus.png"
ONFLOOR_BLAST_MINUS = "./graphisme/items/blue flame.png"
ONFLOOR_SPEED_MINUS = "./graphisme/items/sabot.png"
ONFLOOR_BOMB_MINUS = "./graphisme/items/bomb minus.png"
ONFLOOR_HEART = "./graphisme/items/hearth.png"
ONFLOOR_POWER_GLOVE = "./graphisme/items/power glove.png"
ONFLOOR_KICK = "./graphisme/items/boxing_glove.png"
ONFLOOR_FOOTKICK = "./graphisme/items/footkick.png"
ONFLOOR_SPIKE_BOMB = "./graphisme/items/spike bomb.png"
ONFLOOR_SKULL_DISEAS = "./graphisme/items/skull.png"
ONFLOOR_MAX_BOMB_POWER = "./graphisme/items/max flame.png"
ONFLOOR_EGG = ""

# Bombers animation frames path

BOMBERS_ANIMATION_SPRITE = {
    "WHITE": {
        "K.O.": [
            f"./graphisme/bombers sprites/white/defeat/sprite_  ({i}).png"
            for i in range(1, 8)
        ],
        "Walk_up": [
            f"./graphisme/bombers sprites/white/walk/up/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_down": [
            f"./graphisme/bombers sprites/white/walk/down/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_left": [
            f"./graphisme/bombers sprites/white/walk/left/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
        "Walk_right": [
            f"./graphisme/bombers sprites/white/walk/right/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
    },
    "BLACK": {
        "K.O.": [
            f"./graphisme/bombers sprites/black/defeat/sprite_ ({i}).png"
            for i in range(1, 11)
        ],
        "Walk_up": [
            f"./graphisme/bombers sprites/black/walk/up/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_down": [
            f"./graphisme/bombers sprites/black/walk/down/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_left": [
            f"./graphisme/bombers sprites/black/walk/left/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
        "Walk_right": [
            f"./graphisme/bombers sprites/black/walk/right/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
    },
    "RED": {
        "K.O.": [
            f"./graphisme/bombers sprites/red/defeat/sprite_ ({i}).png"
            for i in range(1, 8)
        ],
        "Walk_up": [
            f"./graphisme/bombers sprites/red/walk/up/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_down": [
            f"./graphisme/bombers sprites/red/walk/down/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_left": [
            f"./graphisme/bombers sprites/red/walk/left/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
        "Walk_right": [
            f"./graphisme/bombers sprites/red/walk/right/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
    },
    "BLUE": {
        "K.O.": [
            f"./graphisme/bombers sprites/blue/defeat/sprite_ ({i}).png"
            for i in range(1, 8)
        ],
        "Walk_up": [
            f"./graphisme/bombers sprites/blue/walk/up/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_down": [
            f"./graphisme/bombers sprites/blue/walk/down/sprite_ ({i}).png"
            for i in range(1, 3)
        ],
        "Walk_left": [
            f"./graphisme/bombers sprites/blue/walk/left/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
        "Walk_right": [
            f"./graphisme/bombers sprites/blue/walk/right/sprite_ ({i}).png"
            for i in range(1, 4)
        ],
    },
}

# SFX PATH

mixer.init()
VOICE_GO = mixer.Sound("./DS DSi - Bomberman - Voices/Go!!.wav")
VOICE_READY = mixer.Sound("./DS DSi - Bomberman - Voices/Ready!.wav")
VOICE_HURRY_UP = mixer.Sound("./DS DSi - Bomberman - Voices/Hurry Up!.wav")
VOICE_DRAW = mixer.Sound("./DS DSi - Bomberman - Voices/It's A Draw!.wav")

# jacket


# control map

# XBX 360 ; XBX ONE
CONTROL_MAP_XBX = {
    "HAT": True,
    "A": 0,
    "B": 1,
    "X": 2,
    "Y": 3,
    "LB": 4,
    "RB": 5,
    "START": 7,
}

# PS4
CONTROL_MAP_PS = {
    "HAT": False,
    "A": 0,  # alias cross
    "B": 1,  # alias circle
    "X": 2,  # alias square
    "Y": 3,  # alias triangle
    "LB": 9,
    "RB": 10,
    "START": 6,
    "D-PAD UP": 11,
    "D-PAD DOWN": 12,
    "D-PAD LEFT": 13,
    "D-PAD RIGHT": 14,
}
