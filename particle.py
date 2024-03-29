import pygame
import math
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Particle:
    def __init__(self, pos, radius, mass):
        self.pos = pos
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.radius = radius
        self.mass = mass

    def update(self, delta):
        for i in range(2):
            self.velocity[i] += self.acceleration[i] * delta
            self.pos[i] += self.velocity[i] * delta

    def collide(self, other_particle):
        dx = other_particle.pos[0] - self.pos[0]
        dy = other_particle.pos[1] - self.pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance < self.radius + other_particle.radius:
            
            total_mass = self.mass + other_particle.mass
            v1x = (self.velocity[0] * (self.mass - other_particle.mass) + 2 * other_particle.mass * other_particle.velocity[0]) / total_mass
            v1y = (self.velocity[1] * (self.mass - other_particle.mass) + 2 * other_particle.mass * other_particle.velocity[1]) / total_mass
            v2x = (other_particle.velocity[0] * (other_particle.mass - self.mass) + 2 * self.mass * self.velocity[0]) / total_mass
            v2y = (other_particle.velocity[1] * (other_particle.mass - self.mass) + 2 * self.mass * self.velocity[1]) / total_mass
            
            self.velocity = [v1x, v1y]
            other_particle.velocity = [v2x, v2y]

class Plane:
    g = 9.8

    def __init__(self, angle):
        self.angle = angle

    def force(self, mass=1):
        
        force_x = mass * Plane.g * math.sin(self.angle)
        force_y = mass * Plane.g * math.cos(self.angle)
        force_z = -mass * Plane.g * math.cos(self.angle)  
        return force_x, force_y, force_z

def main():
    global SCREEN_HEIGHT
    global SCREEN_WIDTH

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("")
    clock = pygame.time.Clock()

   
    angle_degrees = 10
    angle_radians = math.radians(angle_degrees)
    num_particles = 150
    particles = []

    
    plane = Plane(angle_radians)

   
    for _ in range(num_particles):
        particle_pos = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        particle_radius = random.randint(5, 10)
        particle_mass = particle_radius ** 2  
        particle = Particle(particle_pos, particle_radius, particle_mass)
        particles.append(particle)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        
        force_x, force_y, force_z = plane.force()

        
        for particle in particles:
            particle.acceleration = [force_x / particle.mass, force_y / particle.mass, force_z / particle.mass]
            particle.update(.20)

            if not (0<particle.pos[0]<SCREEN_WIDTH):
                particle.velocity[0] *= -1

            if not (0<particle.pos[1]<SCREEN_HEIGHT):
                particle.velocity[1] *= -1

           
            for other_particle in particles:
                if particle != other_particle:
                    particle.collide(other_particle)

            
            pygame.draw.circle(screen, BLACK, (int(particle.pos[0]), int(particle.pos[1])), particle.radius)

        pygame.display.flip()
        

    pygame.quit()


main()
