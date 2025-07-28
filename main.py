import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from CONSTANTS import COLOUR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SIM_HEIGHT, SIM_WIDTH, SIM_BORDER_WIDTH, MAX_PARTICLES
from fluidsim import FluidSim


def main():
    ## Initialisations
    # Pygame & Physics Sim
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    simulation_box = pygame.Rect(SCREEN_WIDTH - SIM_WIDTH - (SCREEN_HEIGHT - SIM_HEIGHT)//2, (SCREEN_HEIGHT - SIM_HEIGHT)//2, SIM_WIDTH, SIM_HEIGHT)
    clock = pygame.time.Clock()
    fluid_sim = FluidSim(screen, simulation_box)
    fluid_sim.generate_particles_grid(particles=1000, spacing=7)


    ## Visual
    # TODO: 
    # - Move Visuals to separate file
    # - Add constants for UI formatting
    # - Create constants for margins and positions
    font = pygame.font.SysFont("Arial", 18)
    pygame.display.set_caption("Particle Fluid Simulation - Alpha2749")
    simulation_box_view = simulation_box.inflate(SIM_BORDER_WIDTH+2, SIM_BORDER_WIDTH+2)

    # UI Elements
    slider_particles_to_spawn = Slider(win=screen, x=25, y=145, width=200, height=20, min=1, max=MAX_PARTICLES, step=10, initial=MAX_PARTICLES, colour=COLOUR.UI_BUTTON_BACKGROUND, handleColour=COLOUR.UI_BUTTON_TEXT)
    slider_gravity = Slider(win=screen, x=25, y=210, width=200, height=20, min=0, max=20, step=0.01, initial=9.81, colour=COLOUR.UI_BUTTON_BACKGROUND, handleColour=COLOUR.UI_BUTTON_TEXT)
    slider_drag_coefficient = Slider(win=screen, x=25, y=275, width=200, height=20, min=0.95, max=1.05, step=0.01, initial=1, colour=COLOUR.UI_BUTTON_BACKGROUND, handleColour=COLOUR.UI_BUTTON_TEXT)
    slider_mouse_strength = Slider(win=screen, x=25, y=350, width=200, height=20, min=2000, max=12000, step=100, initial=10000, colour=COLOUR.UI_BUTTON_BACKGROUND, handleColour=COLOUR.UI_BUTTON_TEXT)

    def spawn_particles():
        fluid_sim.generate_particles_grid(particles=slider_particles_to_spawn.getValue(), spacing=7)

    clear_button = Button(win=screen, x=15, y=30, width=150, height=40, text='Clear Simulation', font = font, fontSize=20, margin=5, inactiveColour=COLOUR.UI_BUTTON_BACKGROUND, hoverColour=COLOUR.UI_BUTTON_HOVER, pressedColour=COLOUR.UI_BUTTON_TEXT, radius=2, onClick=fluid_sim.clear_simulation)
    spawn_button = Button(win=screen, x=15+150+10, y=30, width=150, height=40, text='Spawn Grid', font = font, fontSize=20, margin=5, inactiveColour=COLOUR.UI_BUTTON_BACKGROUND, hoverColour=COLOUR.UI_BUTTON_HOVER, pressedColour=COLOUR.UI_BUTTON_TEXT, radius=2, onClick=spawn_particles)

    ## Main loop
    while True:
        ## User inputs
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
        
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_buttons = pygame.mouse.get_pressed()

        ## Draw base elements
        # TODO: 
        # - Move to separate file
        screen.fill(COLOUR.BLACK)
        label_particles_to_spawn = font.render("Particles to spawn", True, COLOUR.WHITE)
        value_particles_to_spawn = font.render(f"{slider_particles_to_spawn.getValue()} Particles", True, COLOUR.WHITE)
        label_gravity = font.render("Gravity", True, COLOUR.WHITE)
        value_gravity = font.render(f"{slider_gravity.getValue():.2f} m/s^2 - (9.81 for Earth, 1.62 for Moon)", True, COLOUR.WHITE)
        label_drag_coefficient = font.render("Drag Coefficient", True, COLOUR.WHITE)
        value_drag_coefficient = font.render(f"{slider_drag_coefficient.getValue():.2f} % Energy retained from friction", True, COLOUR.WHITE)
        label_mouse_strength = font.render("Mouse Strength (Repulsion & Attraction)", True, COLOUR.WHITE)
        value_mouse_strength = font.render(f"{slider_mouse_strength.getValue()} Unitless... (Play around!)", True, COLOUR.WHITE)
        label_controls1 = font.render("Left Click - Attract Particles to Cursor", True, COLOUR.WHITE)
        label_controls2 = font.render("Right Click - Repel Particles from Cursor", True, COLOUR.WHITE)
        pygame.draw.rect(screen, COLOUR.BOUNDING_BOX, simulation_box_view, width=SIM_BORDER_WIDTH)
        fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, COLOUR.WHITE)

        # blut all UI elements
        blittable = [(fps_text, (15+150+10+150+15, 38)), 
                     (label_particles_to_spawn, (15, 110)), 
                     (value_particles_to_spawn, (250, 145)), 
                     (label_gravity, (15, 175)), 
                     (value_gravity, (250, 210)),
                     (label_drag_coefficient, (15, 245)), 
                     (value_drag_coefficient, (250, 275)),
                     (label_mouse_strength, (15, 320)),
                     (value_mouse_strength, (250, 350)),
                     (label_controls1, (15, 650)),
                     (label_controls2, (15, 685))
        ]
        for i in blittable:
            screen.blit(i[0], i[1]) 
        

        ## Update and draw the fluid simulation
        dt = clock.tick(FPS) / 1000

        fluid_sim.update(dt, mouse_pos, mouse_buttons, gravity=slider_gravity.getValue(), drag_coefficient=slider_drag_coefficient.getValue(), mouse_strength=slider_mouse_strength.getValue())
        fluid_sim.draw()
        pygame_widgets.update(events)
        pygame.display.flip()

if __name__ == "__main__":
    main()
