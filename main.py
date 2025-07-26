import pygame
from CONSTANTS import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOURS
from fluidsim import FluidSim

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()


    while True:
        screen.fill(COLOURS.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.draw.circle(screen, COLOURS.BLUE, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2), 20, width=0)

        dt = clock.tick(FPS) / 1000.0

        pygame.display.flip()

if __name__ == "__main__":
    main()
