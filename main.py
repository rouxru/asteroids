import pygame
from constants import *
from utils import init_text
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
    init_text()
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updateables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    Player.containers = (updateables, drawables)
    Asteroid.containers = (updateables, drawables, asteroids)
    AsteroidField.containers = (updateables,)
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updateables.update(dt=dt)
        for asteroid in asteroids:
            if asteroid.is_colliding(obj=player):
                print("Game over!")
                return
        for drawable in drawables:
            drawable.draw(screen=screen)
        pygame.display.flip()
        dt = clock.tick() / 1000


if __name__ == "__main__":
    main()
