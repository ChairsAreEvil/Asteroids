import pygame
from circleshape import CircleShape
from constants import *

class ShieldPowerUp(CircleShape):
    containers = ()

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
            pygame.draw.circle(screen, "cadetblue1", self.position, self.radius)
            pygame.draw.circle(screen, "cyan", self.position, self.radius, LINE_WIDTH + 2)

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


            # despawn when off-screen
            # margin = 80
            # if (self.position.x < -margin or self.position.x > SCREEN_WIDTH + margin or
                # self.position.y < -margin or self.position.y > SCREEN_HEIGHT + margin):
                  # print("Killed shield at", self.position)
                  # self.kill()