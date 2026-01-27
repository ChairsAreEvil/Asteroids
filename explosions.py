import pygame
from constants import *
from circleshape import CircleShape

class Explosion(CircleShape):
    containers = ()
    
    def __init__(self, x, y, radius, small = False):
        super().__init__(x, y, radius)
        self.small = small
        
        self.lifetime = 0.2
        self.timer = self.lifetime
        self.start_radius = radius

        size = int(radius * 2 + 100)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
            return
        
        t = 1 - (self.timer / self.lifetime)

        self.radius = self.start_radius * (1.0 + 0.95 * t)

        self.alpha = int(255 * (1 - t)**2)

        r = int(255 * (1 - t))
        g = 255
        b = 0

        self.colour_main = (r, g, b, self.alpha)

        g2 = min(255, g + int(80 * (1 - t)))
        self.colour_secondary = (127, g2, b, self.alpha)


        self._redraw_image()

    def _redraw_image(self):
        self.image.fill((0, 0, 0, 0))

        center = (self.image.get_width() // 2, self.image.get_height() // 2)
        r = max(1, int(self.radius))

        c1 = self.colour_main
        c2 = self.colour_secondary
        

        if self.small:
            pygame.draw.circle(self.image, c1, center, max(1, r - 10), LINE_WIDTH)
            pygame.draw.circle(self.image, c2,  center, r, LINE_WIDTH)
            pygame.draw.circle(self.image, c1, center, r + 10, LINE_WIDTH)
        else:
            pygame.draw.circle(self.image, c1, center, r, LINE_WIDTH)

    def draw(self, screen):
        self.rect.center = (int(self.position.x), int(self.position.y))
        screen.blit(self.image, self.rect)
