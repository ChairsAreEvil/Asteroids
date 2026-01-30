import pygame
import random
from asteroid import Asteroid
from shieldpowerup import ShieldPowerUp
from clearpowerup import ClearAsteroidsPowerUp
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, shields_group):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.shields_group = shields_group

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def spawn_shield(self, position, velocity):
        radius = 15
        shield = ShieldPowerUp(position.x, position.y, radius)
        shield.velocity = velocity * 0.75

    def spawn_clearer(self, position, velocity):
        radius = 15
        bomb = ClearAsteroidsPowerUp(position.x, position.y, radius)
        bomb.velocity = velocity * 0.7

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)

            r = random.random()
            if r < CLEAR_SPAWN_CHANCE:
                self.spawn_clearer(position, velocity)
            elif r < SHIELD_SPAWN_CHANCE and len(self.shields_group) < 2:
                self.spawn_shield(position, velocity)
            else:
                self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)