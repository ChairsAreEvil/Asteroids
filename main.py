import pygame
import sys
import random
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosions import Explosion

import os



def load_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except ValueError:
        return 0
    
def save_high_score(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except OSError:
        pass


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    font = pygame.font.Font(None, 36)

    score = 0
    high_score = load_high_score()

    game_over = False
    
    stars = []
    for _ in range(NUM_STARS):
        x = random.randrange(0, SCREEN_WIDTH)
        y = random.randrange(0, SCREEN_HEIGHT)
        speed = random.choice([1, 1.5, 2, 2.5, 3])
        stars.append([x, y, speed])
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)

    field = AsteroidField()
    ship = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


    def points_per_asteroid(asteroid):
        r = asteroid.radius
        if r >= 60:
            return 50
        elif r >= 40:
            return 25
        else:
            return 10
    
    
    while 1 == 1:
        log_state()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
                    if event.key == pygame.K_r:
                        main()
                        return
                
        for star in stars:
                star[1] += star[2]

                if star[1] > SCREEN_HEIGHT:
                    star[0] = random.randrange(0, SCREEN_WIDTH)
                    star[1] = 0
            
        screen.fill("black")
        
        for x, y, speed in stars:
            size = speed
            screen.fill("white", (x, y, size, size))
        
        if not game_over:
            updatable.update(dt)
            
            for asteroid in asteroids:
                if asteroid.collides_with(ship):
                    log_event("player_hit")
                    print("Game over!")
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    game_over = True

            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        score += points_per_asteroid(asteroid)
                        asteroid.split()

            for draw in drawable:
                draw.draw(screen)
        else:
            # --- game over screen ---

            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            info_text      = font.render("R: restart   Q: quit", True, (255, 255, 255))
            score_text     = font.render(f"Score: {score}", True, (255, 255, 255))
            hs_text        = font.render(f"High:  {high_score}", True, (255, 255, 255))

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - 60))
            screen.blit(score_text,     (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - 20))
            screen.blit(hs_text,        (SCREEN_WIDTH // 2 - hs_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 20))
            screen.blit(info_text,      (SCREEN_WIDTH // 2 - info_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 60))
        


        if not game_over:
            score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
            hs_surf    = font.render(f"High:  {high_score}", True, (255, 255, 255))

            screen.blit(score_surf, (10,10))
            screen.blit(hs_surf,    (10, 40))

        pygame.display.flip()
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
