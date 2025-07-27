import pygame
from CONSTANTS import COLOUR, POSITION, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SIM_HEIGHT, SIM_WIDTH, SIM_BORDER_WIDTH
from fluidsim import FluidSim


def main():
    ## Initialisations
    # Pygame & Physics Sim
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    simulation_box = pygame.Rect((SCREEN_WIDTH - SIM_WIDTH) // 2, (SCREEN_HEIGHT - SIM_HEIGHT) // 2, SIM_WIDTH, SIM_HEIGHT)
    clock = pygame.time.Clock()
    fluid_sim = FluidSim(screen, simulation_box)
    fluid_sim.generate_particles_grid(spacing=7)

    # Visual
    font = pygame.font.SysFont("Arial", 18)
    pygame.display.set_caption("FLIP Fluid Simulation - Alpha2749")
    simulation_box_view = simulation_box.inflate(SIM_BORDER_WIDTH+2, SIM_BORDER_WIDTH+2)

    # Main Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    # modify some parameters
                    pass
                
        # Draw base elements
        screen.fill(COLOUR.BLACK)
        pygame.draw.rect(screen, COLOUR.RED, simulation_box_view, width=SIM_BORDER_WIDTH)
        fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, COLOUR.WHITE)
        screen.blit(fps_text, POSITION.TOP_LEFT) 
        
        # Update and draw the fluid simulation
        dt = clock.tick(FPS) / 1000
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_buttons = pygame.mouse.get_pressed()

        fluid_sim.update(dt, mouse_pos, mouse_buttons)
        fluid_sim.draw()

        pygame.display.flip()

if __name__ == "__main__":
    main()
