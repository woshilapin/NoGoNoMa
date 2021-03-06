TITLE = "RuToPy RL"
FONT = "fonts/16x16_sm_ascii.png, size=16x16, codepage=437"

RAW_FILES = '/raws'
TILE_DIR = 'tileset'

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60
MAX_MENU_SIZE_WIDTH = 80 // 4 * 3

MAP_SCREEN_WIDTH = 80
MAP_SCREEN_HEIGHT = 50

SHOW_BOUNDARIES = False  # Debug
SHOW_MAPGEN_VISUALIZER = False    # debug
MAPGEN_VISUALIZER_TIMER = 10

BUILDER_MAX_NB_TRIES = 3
BUILDER_MIN_PATH_BETWEEN_START_EXIT_TEST = 20

BASE_MONSTER_INITIATIVE = 2
DEFAULT_INITIATIVE_GAIN = 6
DEFAULT_INITIATIVE_TICK = 1
MIN_DISTANCE_TO_BE_ACTIVE = 20

DEFAULT_MOVE_INITIATIVE_COST = 6
DEFAULT_FIGHT_INITIATIVE_COST = 8
DEFAULT_WAIT_INITIATIVE_COST = 1
DEFAULT_ITEM_USE_INITIATIVE_COST = 4

DEFAULT_LANGUAGE = 'en'
FPS = 100

UI_STATS_INFO_LINE = 51
UI_LOG_FIRST_LINE = 53
LOG_LIMIT_DEATH_SCREEN = 10

UI_HP_BAR_WIDTH = 10
COLOR_HP_BAR_BACKGROUND = 'darker red'
COLOR_HP_BAR_VALUE = 'lighter red'
COLOR_TEXT_HP_BAR = 'grey'

UI_XP_BAR_WIDTH = 20
COLOR_XP_BAR_BACKGROUND = 'darker orange'
COLOR_XP_BAR_VALUE = 'light yellow'
COLOR_TEXT_XP_BAR = 'grey'

MAX_DEPTH = 6
MAX_ROOMS = 30
MIN_SIZE = 6
MAX_SIZE = 10

MAX_MONSTERS_ROOM = 3
MAX_ITEMS_ROOM = 2

XP_PER_LEVEL = 10
XP_MULTIPLIER = 1
XP_GAIN_PER_MONSTER_LVL = 1
XP_GAIN_MULTIPLIER = 1
XP_PER_DEPTH = 5
XP_DEPTH_MULTIPLIER = 1

DEFAULT_VISIBILITY = 10
BLOOD_ON_GROUND_CHANCE = 15

DEFAULT_HIT_POINTS = 10
DEFAULT_MONSTER_HIT_POINTS = 8
DEFAULT_MANA_POINTS = 4
DEFAULT_NO_SKILL_VALUE = -4
DEFAULT_MONSTER_BODY_ATTRIBUTE = 2
DEFAULT_MONSTER_MIGHT_ATTRIBUTE = 3
DEFAULT_MONSTER_QUICKNESS_ATTRIBUTE = 2
DEFAULT_MONSTER_WITS_ATTRIBUTE = 3
DEFAULT_PLAYER_BODY_ATTRIBUTE = 4
DEFAULT_PLAYER_MIGHT_ATTRIBUTE = 4
DEFAULT_PLAYER_QUICKNESS_ATTRIBUTE = 4
DEFAULT_PLAYER_WITS_ATTRIBUTE = 4

DEFAULT_TRAP_DETECTION_DIFFICULTY = 60
DEFAULT_TRAP_DODGE = 100

DEFAULT_NATURAL_ATTACK_CHOICE = 50
DEFAULT_MIN_DMG = 1
DEFAULT_MAX_DMG = 3

COLOR_PLAYER_INFO_OK = 'lighter blue'
COLOR_PLAYER_INFO_NOT = 'light orange'
COLOR_MAJOR_INFO = 'orange'
COLOR_DEADLY_INFO = 'red'
COLOR_SYS_MSG = 'yellow'
COLOR_INFO_INVENTORY_TEXT = 'white'
COLOR_INFO_UNSELECTABLE_ITEMS_INVENTORY = 'gray'
COLOR_INFO_INVENTORY_SELECTED_ITEM = 'light yellow'
COLOR_INVENTORY_OPTION = 'lighter cyan'
COLOR_INFO_ATTRIBUTE_INVENTORY_MENU = 'dark green'
COLOR_INFO_SELECTED_ITEM_IN_INVENTORY = 'light yellow'
COLOR_MENU_BASE = 'white'
COLOR_MENU_SUBTITLE_BASE = 'yellow'
COLOR_MAIN_MENU_OPTIONS = 'orange'
COLOR_MAIN_MENU_TITLE = 'yellow'
COLOR_MENU_BACKGROUND_BASE = 'gray'

COLOR_PARTICULE_MISS = 'white'
COLOR_PARTICULE_HIT = 'orange'
COLOR_PARTICULE_NO_HURT = 'blue'
COLOR_PARTICULE_HEAL = 'green'
LOW_RADIUS = 3
MEDIUM_RADIUS = 5
HIGH_RADIUS = 7
HUGE_RADIUS = 9

POTION_COLORS = ["RED_COLOR", "ORANGE_COLOR", "YELLOW_COLOR", "GREEN_COLOR_F", "BROWN_COLOR", "INDIGO_COLOR",
                 "VIOLET_COLOR_F"]
POTION_ADJECTIVES = ["SWIRLING_ADJ", "EFFERVESCENT_ADJ", "SLIMEY_ADJ", "OILEY_ADJ", "VISCOUS_ADJ", "SMELLY_ADJ",
                     "GLOWING_ADJ"]
