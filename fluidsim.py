import numpy as np
import pygame
import pygame.gfxdraw
from CONSTANTS import COLOUR, VELOCITY, GRAVITY, DAMPING_FACTOR, PARTICLE_RADIUS, MAX_PARTICLES

class FluidSim:
    def __init__(self, screen, sim_box):
        self.screen = screen
        self.sim_box = sim_box
        self.particles = []
    
    def generate_particle_grid(self, spacing=20):
        x_start = self.sim_box.left + PARTICLE_RADIUS
        y_start = self.sim_box.top + PARTICLE_RADIUS
        x_end = self.sim_box.right - PARTICLE_RADIUS
        y_end = self.sim_box.bottom - PARTICLE_RADIUS

        for x in range(x_start, x_end, spacing):
            for y in range(y_start, y_end, spacing):
                pos = pygame.Vector2(x, y)
                vel = pygame.Vector2(0, 0)
                self.particles.append(Particle(pos, vel, self.screen, self.sim_box))

    def add_particle(self, position, velocity):
        if len(self.particles) < MAX_PARTICLES:
            particle = Particle(position, velocity, self.screen, self.sim_box)
            self.particles.append(particle)

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)

    def draw(self):
        for particle in self.particles:
            particle.draw()

class Particle:
    def __init__(self, position, velocity, screen, sim_box):
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.sim_box = sim_box
    
    def update(self, dt):
        self.velocity += VELOCITY.DOWN * GRAVITY * 100 * dt 
        self.position += self.velocity * dt

        left   = self.sim_box.left + PARTICLE_RADIUS
        right  = self.sim_box.right - PARTICLE_RADIUS
        top    = self.sim_box.top + PARTICLE_RADIUS
        bottom = self.sim_box.bottom - PARTICLE_RADIUS

        if self.position.x < left:
            self.position.x = left
            self.velocity.x *= -DAMPING_FACTOR
        elif self.position.x > right:
            self.position.x = right
            self.velocity.x *= -DAMPING_FACTOR

        if self.position.y < top:
            self.position.y = top
            self.velocity.y *= -DAMPING_FACTOR
        elif self.position.y > bottom:
            self.position.y = bottom
            self.velocity.y *= -DAMPING_FACTOR

        if abs(self.velocity.y) < 0.01:
            self.velocity.y = 0

    def draw(self):
        pygame.draw.circle(self.screen, COLOUR.BLUE, (int(self.position.x), int(self.position.y)), PARTICLE_RADIUS)
        #self._draw_soft_circle(self.screen, COLOUR.BLUE, self.position, PARTICLE_RADIUS)

    def _draw_soft_circle(self, surface, colour, position, radius):
        x, y = int(position.x), int(position.y)
        pygame.gfxdraw.aacircle(surface, x, y, radius, colour) 
        pygame.gfxdraw.filled_circle(surface, x, y, radius, colour) 
