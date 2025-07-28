import pygame
import pygame.gfxdraw
from CONSTANTS import (
    COLOUR, VELOCITY, GRAVITY, DAMPING_FACTOR,
    PARTICLE_RADIUS, MAX_PARTICLES, DRAG_COEFFICIENT,
    REPULSION_SMOOTHING, REPULSION_STRENGTH, MAX_PARTICLE_VELOCITY,
    MOUSE_ATTRACT_RADIUS, MOUSE_ATTRACT_STRENGTH
)

## TODO:
## - Refactor/ clean up code
## - Move user input handling out of here

class FluidSim:
    def __init__(self, screen, sim_box):
        self.screen = screen
        self.sim_box = sim_box
        self.particles = []
        self.grid = SpatialGrid(cell_size=PARTICLE_RADIUS * 2)
        self.bounds = {
            'left': self.sim_box.left + PARTICLE_RADIUS,
            'right': self.sim_box.right - PARTICLE_RADIUS,
            'top': self.sim_box.top + PARTICLE_RADIUS,
            'bottom': self.sim_box.bottom - PARTICLE_RADIUS
        }
    
    def clear_simulation(self):
        self.particles = []
    
    def generate_particles_grid(self, particles=800, spacing=7):
        row = 0
        count = 0
        y = self.bounds['top']

        while y < self.bounds['bottom'] and count < particles:
            offset = spacing // 2 if row % 2 else 0
            x = self.bounds['left'] + offset

            while x < self.bounds['right'] and count < particles:
                if len(self.particles) >= MAX_PARTICLES:
                    return
                position = pygame.Vector2(x, y)
                self.add_particle(position, pygame.Vector2(0, 0))
                count += 1
                x += spacing

            y += spacing
            row += 1

    def add_particle(self, position, velocity):
        if len(self.particles) < MAX_PARTICLES:
            self.particles.append(Particle(position, velocity, self.screen, self.bounds))

    def _apply_external_forces(self):
        for a in self.particles:
            for b in self.grid.get_neighbors(a):
                if a is b:
                    continue

                delta = a.position - b.position
                dist = delta.length()
                min_dist = PARTICLE_RADIUS * 2

                avg_velocity = (a.velocity + b.velocity) * 0.5
                a.velocity = a.velocity.lerp(avg_velocity, 0.1)
                b.velocity = b.velocity.lerp(avg_velocity, 0.1)

                if 0 < dist < min_dist:
                    direction = delta.normalize()
                    force = direction * (1 - dist / min_dist) * REPULSION_STRENGTH
                    a.velocity += force
                    b.velocity -= force

                    overlap = min_dist - dist
                    correction = direction * (overlap * 0.5 * REPULSION_SMOOTHING)
                    a.position += correction
                    b.position -= correction

    def update(self, dt, mouse_pos=None, mouse_buttons=None):
        self.grid.clear()
        for particle in self.particles:
            self.grid.insert(particle)
        
        self._apply_external_forces()
        for particle in self.particles:
            particle.update(dt, mouse_pos, mouse_buttons)

    def draw(self):
        for particle in self.particles:
            particle.draw()


class Particle:
    def __init__(self, position, velocity, screen, sim_bounds):
        self.position = position
        self.velocity = velocity
        self.screen = screen
        self.bounds = sim_bounds

    def update(self, dt, mouse_pos=None, mouse_buttons=None):
        self._apply_gravity(dt)
        self._apply_drag()
        if mouse_pos:
            self._apply_user_forces(dt, mouse_pos, mouse_buttons)
        self._clamp_velocity()

        self.position += self.velocity * dt
        self._clamp_position()

    def _apply_drag(self):
        self.velocity *= DRAG_COEFFICIENT

    def _apply_gravity(self, dt):
        self.velocity += VELOCITY.DOWN * (GRAVITY * 100) * dt

    def _clamp_velocity(self):
        if self.velocity.length_squared() > MAX_PARTICLE_VELOCITY ** 2:
            self.velocity.scale_to_length(MAX_PARTICLE_VELOCITY)

    def _apply_user_forces(self, dt, mouse_pos, mouse_buttons):
        if mouse_pos and mouse_buttons:
            direction = mouse_pos - self.position
            distance = direction.length()
            
            if distance < MOUSE_ATTRACT_RADIUS and distance > 0:
                direction.normalize_ip() 
                strength = 1 - distance / MOUSE_ATTRACT_RADIUS
                
                # TODO: move input handling from here
                if mouse_buttons[0]:  # Left click - attract
                    self.velocity += direction * MOUSE_ATTRACT_STRENGTH * strength * dt
                elif mouse_buttons[2]:  # Right click - repel
                    self.velocity -= direction * MOUSE_ATTRACT_STRENGTH * strength * dt

    def _clamp_position(self):
        if self.position.x < self.bounds['left']:
            self.position.x = self.bounds['left']
            self.velocity.x *= -DAMPING_FACTOR
        elif self.position.x > self.bounds['right']:
            self.position.x = self.bounds['right']
            self.velocity.x *= -DAMPING_FACTOR

        if self.position.y < self.bounds['top']:
            self.position.y = self.bounds['top']
            self.velocity.y *= -DAMPING_FACTOR
        elif self.position.y > self.bounds['bottom']:
            self.position.y = self.bounds['bottom']
            self.velocity.y *= -DAMPING_FACTOR

        if abs(self.velocity.y) < 0.01:
            self.velocity.y = 0

    def draw(self):
        self._draw_soft_circle(self.screen, COLOUR.WATER_PARTICLE, self.position, PARTICLE_RADIUS)

    def _draw_soft_circle(self, surface, colour, position, radius):
        x, y = int(position.x), int(position.y)
        pygame.gfxdraw.aacircle(surface, x, y, radius, COLOUR.PARTICLE_HIGHLIGHT)
        pygame.gfxdraw.filled_circle(surface, x, y, radius, colour)

class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}

    def _hash(self, position):
        return (int(position.x) // self.cell_size, int(position.y) // self.cell_size)

    def clear(self):
        self.cells.clear()

    def insert(self, particle):
        cell = self._hash(particle.position)
        self.cells.setdefault(cell, []).append(particle)

    def get_neighbors(self, particle):
        x, y = self._hash(particle.position)
        neighbors = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbors.extend(self.cells.get((x + dx, y + dy), []))

        return neighbors
