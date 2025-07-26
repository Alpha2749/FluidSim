import pygame
from CONSTANTS import COLOUR, POSITION, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SIM_HEIGHT, SIM_WIDTH, SIM_BORDER_WIDTH
from fluidsim import FluidSim


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    simulation_box = pygame.Rect((SCREEN_WIDTH - SIM_WIDTH) // 2, (SCREEN_HEIGHT - SIM_HEIGHT) // 2, SIM_WIDTH, SIM_HEIGHT)
    simulation_box_view = simulation_box.inflate(SIM_BORDER_WIDTH+2, SIM_BORDER_WIDTH+2)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    pygame.display.set_caption("FLIP Fluid Simulation - Alpha2749")


    fluid_sim = FluidSim(screen, simulation_box)
    fluid_sim.generate_particle_grid(spacing=20)

    while True:
        screen.fill(COLOUR.BLACK)
        pygame.draw.rect(screen, COLOUR.RED, simulation_box_view, width=SIM_BORDER_WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, COLOUR.WHITE)
        screen.blit(fps_text, POSITION.TOP_LEFT) 
            
        dt = clock.tick(FPS) / 1000

        fluid_sim.update(dt)
        fluid_sim.draw()

        pygame.display.flip()

if __name__ == "__main__":
    main()
