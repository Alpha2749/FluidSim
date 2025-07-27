import pygame

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
FLUID_DENSITY = 100.0
GRAVITY = 9.81                  # Acceleration due to Gravity i.e. 9.81 m/s^2 for Earth, or 1.62 m/s^2 for the Moon
DAMPING_FACTOR = 0.95           # Damping factor for velocity after collision i.e 0.90 means 10% of velocity is lost after collision
REPULSION_STRENGTH = 400        # Strength of repulsion force between particles

MOUSE_ATTRACT_RADIUS = 250
MOUSE_ATTRACT_STRENGTH = 10000

## Don't really need to touch these
SIM_WIDTH = 600          
SIM_HEIGHT = 600
SIM_BORDER_WIDTH = 3            
PARTICLE_SPACING = 8     
PARTICLE_RADIUS = 6
MAX_PARTICLES = 1000
DRAG_COEFFICIENT = 1
REPULSION_SMOOTHING = 0.4
MAX_PARTICLE_VELOCITY = 1200


####################
### COLOUR CODES ###
####################
class COLOUR:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

####################
#### POSITIONS #####
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