import numpy as np
import pygame
import pygame.gfxdraw
from CONSTANTS import COLOUR, VELOCITY, GRAVITY, DAMPING_FACTOR, PARTICLE_RADIUS, MAX_PARTICLES, DRAG_COEFFICIENT, REPULSION_SMOOTHING, REPULSION_STRENGTH, MAX_PARTICLE_VELOCITY, MOUSE_ATTRACT_RADIUS, MOUSE_ATTRACT_STRENGTH

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
        if cell not in self.cells:
            self.cells[cell] = []
        self.cells[cell].append(particle)

    def get_neighbors(self, particle):
        x, y = self._hash(particle.position)
        neighbors = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cell = (x + dx, y + dy)
                if cell in self.cells:
                    neighbors.extend(self.cells[cell])

        return neighbors

class FluidSim:
    def __init__(self, screen, sim_box):
        self.screen = screen
        self.sim_box = sim_box
        self.particles = []
        self.grid = SpatialGrid(cell_size=PARTICLE_RADIUS * 2)
    
    def generate_particle_grid(self, spacing=20):
        x_start = self.sim_box.left + PARTICLE_RADIUS
        y_start = self.sim_box.top + PARTICLE_RADIUS
        x_end = self.sim_box.right - PARTICLE_RADIUS
        y_end = self.sim_box.bottom - PARTICLE_RADIUS

        row = 0
        for y in range(y_start, y_end, spacing):
            offset = spacing // 2 if row % 2 == 1 else 0 
            for x in range(x_start + offset, x_end, spacing):
                position = pygame.Vector2(x, y)
                velocity = pygame.Vector2(0, 0)
                if len(self.particles) < MAX_PARTICLES:
                    self.add_particle(position, velocity)
                else:
                    return
            row += 1

    def add_particle(self, position, velocity):
        if len(self.particles) < MAX_PARTICLES:
            particle = Particle(position, velocity, self.screen, self.sim_box)
            self.particles.append(particle)
    
    def _apply_external_forces(self):
        for p1 in self.particles:
            neighbors = self.grid.get_neighbors(p1)
            for p2 in neighbors:
                if p1 is p2:
                    continue
                delta = p1.position - p2.position
                dist = delta.length()
                min_dist = PARTICLE_RADIUS * 2
                                
                avg_velocity = (p1.velocity + p2.velocity) / 2
                p1.velocity = p1.velocity.lerp(avg_velocity, 0.1)
                p2.velocity = p2.velocity.lerp(avg_velocity, 0.1)


                if 0 < dist < min_dist:
                    direction = delta.normalize()
                    force = direction * (1 - dist / min_dist) * REPULSION_STRENGTH
                    p1.velocity += force
                    p2.velocity -= force
                
                if dist < min_dist and dist > 0:
                    overlap = min_dist - dist
                    correction = delta.normalize() * (overlap / 2)

                    p1.position += correction * REPULSION_SMOOTHING
                    p2.position -= correction * REPULSION_SMOOTHING
                    

    def update(self, dt, mouse_pos=None):
        self.grid.clear()
        for p in self.particles:
            self.grid.insert(p)
        self._apply_external_forces()
        for particle in self.particles:
            particle.update(dt, mouse_pos)

    def draw(self):
        for particle in self.particles:
            particle.draw()

class Particle:
    def __init__(self, position, velocity, screen, sim_box):
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.sim_box = sim_box
    
    def update(self, dt, mouse_pos=None):
        self.velocity *= DRAG_COEFFICIENT
        self.velocity += VELOCITY.DOWN * (GRAVITY * 100) * dt 
        if self.velocity.length() > MAX_PARTICLE_VELOCITY:
            self.velocity.scale_to_length(MAX_PARTICLE_VELOCITY)

        if mouse_pos is not None:
            direction = mouse_pos - self.position
            distance = direction.length()
            if distance < MOUSE_ATTRACT_RADIUS and distance != 0:
                direction.normalize_ip()
                strength = (1 - distance / MOUSE_ATTRACT_RADIUS) 
                self.velocity += direction * MOUSE_ATTRACT_STRENGTH * strength * dt

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
        #pygame.draw.circle(self.screen, COLOUR.BLUE, (int(self.position.x), int(self.position.y)), PARTICLE_RADIUS)
        self._draw_soft_circle(self.screen, COLOUR.BLUE, self.position, PARTICLE_RADIUS)

    def _draw_soft_circle(self, surface, colour, position, radius):
        x, y = int(position.x), int(position.y)
        pygame.gfxdraw.aacircle(surface, x, y, radius, COLOUR.GREEN) 
        pygame.gfxdraw.filled_circle(surface, x, y, radius, colour) 
