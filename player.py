import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.shield_active = False
        self.tri_shot_active = False
        self.tri_shot_ammo = 0

# draws the player
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "blue4", self.triangle())
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        if self.shield_active:
            pygame.draw.circle(screen, "cadetblue1", self.position, self.radius + 12, LINE_WIDTH + 1)

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def update(self, dt):
        self.cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

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

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.cooldown > 0:
            return
        self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        base_dir = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.tri_shot_active:
            angles = [-10, 0, 10]
            for angle in angles:
                direction = base_dir.rotate(angle)
                shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
                shot.velocity = direction * PLAYER_SHOOT_SPEED

            self.tri_shot_ammo -= 1
            if self.tri_shot_ammo <= 0:
                self.tri_shot_active = False
        else:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = base_dir * PLAYER_SHOOT_SPEED

