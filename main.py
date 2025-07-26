import pygame
from CONSTANTS import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()


    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = clock.tick(FPS) / 1000.0
        # Sim updates & draws
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
