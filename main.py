import pygame
import random
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosions import Explosion
from shieldpowerup import ShieldPowerUp
from clearpowerup import ClearAsteroidsPowerUp
from trishot import TriShotPowerUp
import os


# --- high score helpers ---
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

# --- game helpers ---
def points_per_asteroid(asteroid):
    r = asteroid.radius
    if r >= 60:
        return 50
    elif r >= 40:
        return 25
    else:
        return 10
    

def handle_events(game_over):
    """Return (running, restart) based on input"""
    restart = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, restart
        
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False, restart
                if event.key == pygame.K_r:
                    restart = True
    return True, restart
    

def update_game(state, dt):
    # stars always move
    for star in state.stars:
        star[1] += star[2]

        if star[1] > SCREEN_HEIGHT:
            star[0] = random.randrange(0, SCREEN_WIDTH)
            star[1] = 0
        
    if not state.game_over:
        state.updatable.update(dt)

        for shield in list(state.shields):
            if shield.collides_with(state.ship):
                state.ship.shield_active = True
                shield.kill()
                break

        for bomb in list(state.clearers):
            if bomb.collides_with(state.ship):
                log_event("clear_asteroids")
                for asteroid in list(state.asteroids):
                    state.score += points_per_asteroid(asteroid)
                    asteroid.create_explosion(asteroid.position.x, asteroid.position.y, asteroid.radius, small=True)
                    asteroid.kill()
                bomb.kill()
                break

        for tri_shot in list(state.tri_shots):
            if tri_shot.collides_with(state.ship):
                state.ship.tri_shot_active = True
                state.ship.tri_shot_ammo += 30
                tri_shot.kill()
                break

        #if player on respawn cooldown
        if state.respawn_timer > 0:
            state.respawn_timer -= dt
        else:
            # player can be hit
            for asteroid in state.asteroids:
                if asteroid.collides_with(state.ship):
                    if state.ship.shield_active:
                        state.ship.shield_active = False
                        log_event("shield_block")
                        asteroid.split()
                    else:
                        log_event("player_hit")
                        state.lives -= 1
                        print(f"Player hit! Lives remaining: {state.lives}")

                        if state.lives <= 0:
                            print("Game over!")
                            if state.score > state.high_score:
                                state.high_score = state.score
                                save_high_score(state.high_score)
                            state.game_over = True
                        else:
                            # respawn: reset ship, start timer
                            state.respawn_timer = 2.0  # seconds of invulnerability
                            state.ship.position.update(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            state.ship.velocity.update(0, 0)
                    break
        
        # shots vs asteroids (only if still alive)
        if not state.game_over:
            for asteroid in list(state.asteroids): # list() avoids modifying while iterating
                for shot in list(state.shots):
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        state.score += points_per_asteroid(asteroid)
                        asteroid.split()
                        break


def draw_game(state):
    screen = state.screen
    font = state.font

    screen.fill("black")

    # stars background
    for x, y, speed in state.stars:
        size = speed
        screen.fill("white", (x, y, size, size))

    if not state.game_over:
        # normal world
        for draw in state.drawable:
            if draw is state.ship and state.respawn_timer > 0:
                t = pygame.time.get_ticks() / 100.0
                if int(t) % 2 == 0:
                    continue
            draw.draw(screen)
            
        score_surf = font.render(f"Score: {state.score}", True, (255, 255, 255))
        hs_surf    = font.render(f"High:  {state.high_score}", True, (255, 255, 255))
        lives_surf = font.render(f"Lives: {state.lives}", True, (255, 255, 255))
        ammo_surf  = font.render(f"Tri-Shot Ammo: {state.ship.tri_shot_ammo}", True, (255, 255, 255))
        screen.blit(score_surf, (10,10))
        screen.blit(hs_surf,    (10, 40))
        screen.blit(lives_surf, (10, 70))
        screen.blit(ammo_surf,  (10, 100))
    else:
        # game over screen
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        info_text      = font.render("R: restart   Q: quit", True, (255, 255, 255))
        score_text     = font.render(f"Score: {state.score}", True, (255, 255, 255))
        hs_text        = font.render(f"High:  {state.high_score}", True, (255, 255, 255))

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - 60))
        screen.blit(score_text,     (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - 20))
        screen.blit(hs_text,        (SCREEN_WIDTH // 2 - hs_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 + 20))
        screen.blit(info_text,      (SCREEN_WIDTH // 2 - info_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 + 60))
    pygame.display.flip()

# --- hold all info for each run ---
class GameState:
    def __init__(self, screen, font, stars,
                 updatable, drawable, asteroids, shots,
                 ship, high_score, shields, clearers, tri_shots):
        self.screen = screen
        self.font = font
        self.stars = stars

        self.updatable = updatable
        self.drawable = drawable
        self.asteroids = asteroids
        self.shots = shots
        self.ship = ship
        self.shields = shields
        self.clearers = clearers
        self.tri_shots = tri_shots

        self.score = 0
        self.high_score = high_score
        self.game_over = False

        self.lives = 3
        self.respawn_timer = 0.0

# --- main entry point ---
def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    font = pygame.font.Font(None, 36)
    high_score = load_high_score()
    
    #stars
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
    shields = pygame.sprite.Group()
    clearers = pygame.sprite.Group()
    tri_shots = pygame.sprite.Group()
    #explosions = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    ShieldPowerUp.containers = (shields, updatable, drawable)
    ClearAsteroidsPowerUp.containers = (clearers, updatable, drawable)
    TriShotPowerUp.containers = (tri_shots, updatable, drawable)

    field = AsteroidField(shields, tri_shots)
    ship = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    # temp shield test:
    # test_shield = ShieldPowerUp(200, 200, 15)
    # test_shield.velocity = pygame.Vector2(60, 30)

    state = GameState(
        screen=screen,
        font=font,
        stars=stars,
        updatable=updatable,
        drawable=drawable,
        asteroids=asteroids,
        shots=shots,
        ship=ship,
        high_score=high_score,
        shields=shields,
        clearers=clearers,
        tri_shots=tri_shots
    )
   

    running = True
    while running:
        log_state()
        
        running, restart = handle_events(state.game_over)
        if not running:
            return
        if restart:
            main()
            return

        update_game(state, dt)
        draw_game(state)
        
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
