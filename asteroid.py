import pygame
import random
from circleshape import CircleShape
from constants import *
from logger import log_event
from explosions import Explosion

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "chocolate4", self.position, self.radius)
        pygame.draw.circle(screen, "chocolate", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def create_explosion(self,x, y, radius, small=False):
        Explosion(x, y, radius, small)
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.create_explosion(self.position.x, self.position.y, self.radius, small=True)
            return
        
        log_event("asteroid_split")
        self.create_explosion(self.position.x, self.position.y, self.radius, small=False)
        
        angle = random.uniform(20, 50)
        new_velocity1 = self.velocity.rotate(angle)
        new_velocity2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid1.velocity = new_velocity1 * 1.2
        asteroid2.velocity = new_velocity2 * 1.2