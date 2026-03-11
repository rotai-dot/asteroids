import pygame 
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot

def main():
#some prints

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

#initializing the game

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

#creating the containers for the sprites

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


#setting the objects containers and initializing game objects

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    #asteroidfields is a clase for spawning new asteroids
    AsteroidField.containers = (updatable,)

    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()


#main game loop
    while True:
        #debugging log and a tool for boot.dev to check
        log_state()

        #check if we close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #overrride all draws on the screen by setting it to black and update the state by dt   
        screen.fill("black")
        updatable.update(dt)

        #we check for every asteroid if they collide with the player and also if they collide with a shot
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    #stop looking for shots hitting an already dead asteroid
                    break
        #after checking everything we draw all objects back into the screen with their updated states
        for sprite in drawable:
            sprite.draw(screen)

        #we wait the time needed to draw maximum of 60 fps
        dt = clock.tick(60)/1000
        #we flip the screen to the frame in buffer
        pygame.display.flip()












if __name__ == "__main__":
    main()
