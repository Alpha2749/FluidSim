import pygame

## TODO:
# - Add visualisation constants (margins, positions, etc)
# - Purge unused constants

###################
## VIS CONSTANTS ##
###################
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60


###################
## SIM CONSTANTS ##
###################
## These are fun to play with!
DAMPING_FACTOR = 0.95           # Damping factor for velocity after collision i.e 0.90 means 10% of velocity is lost after collision
REPULSION_STRENGTH = 400        # Strength of repulsion force between particles

MOUSE_ATTRACT_RADIUS = 250
MOUSE_ATTRACT_STRENGTH = 10000

## Don't really need to touch these
SIM_WIDTH = 600          
SIM_HEIGHT = 600
SIM_BORDER_WIDTH = 3             
PARTICLE_RADIUS = 6
MAX_PARTICLES = 800
REPULSION_SMOOTHING = 0.4
MAX_PARTICLE_VELOCITY = 1500


####################
### COLOUR CODES ###
####################
class COLOUR:
    WHITE = (255, 255, 255)
    BLACK = (10, 10, 10)
    RED = (255, 0, 0)
    CRIMSON_RED = (220, 50, 70)
    SOFT_ORANGE = (255, 160, 70)
    SILVER_GREY = (180, 180, 200)
    DEEP_GOLD = (255, 200, 80)
    GREEN = (0, 255, 0)
    DEEP_AQUA = (50, 120, 150)
    BLUE = (0, 0, 255)
    SKY_BLUE = (135, 206, 235)
    LIGHT_AQUA = (0, 163, 204)
    WATER_PARTICLE_LIGHT = (30, 144, 255)
    WATER_PARTICLE_DARK = (10, 90, 150)
    PARTICLE_HIGHLIGHT = (100, 200, 255)
    WATER_PARTICLE = (10, 90, 150)
    BOUNDING_BOX = (180, 180, 200)
    UI_BUTTON_BACKGROUND = (0, 122, 204)
    UI_BUTTON_HOVER = (0, 142, 234)
    UI_BUTTON_TEXT = (240, 240, 240)

####################
###### OTHER #######
####################
class POSITION:
    TOP_LEFT = pygame.math.Vector2(0, 0)
    TOP_RIGHT = pygame.math.Vector2(SCREEN_WIDTH, 0)
    BOTTOM_LEFT = pygame.math.Vector2(0, SCREEN_HEIGHT)
    BOTTOM_RIGHT = pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
    CENTER = pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

class VELOCITY:
    UP = pygame.math.Vector2(0, -1)
    DOWN = pygame.math.Vector2(0, 1)
    LEFT = pygame.math.Vector2(-1, 0)
    RIGHT = pygame.math.Vector2(1, 0)
    NONE = pygame.math.Vector2(0, 0)

class VISUAL:
    ELEMENT_MARGIN = 15