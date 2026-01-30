import pygame
from circleshape import CircleShape
from constants import *

class TriShotPowerUp(CircleShape):
    containers = ()

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "magenta3", self.position, self.radius)
        pygame.draw.circle(screen, "magenta4", self.position, self.radius, LINE_WIDTH + 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

        # wrap horizontally
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        # wrap vertically
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius