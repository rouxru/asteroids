import itertools

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from explosion import Explosion
from player import Player
from shot import Shot
from utils import init_text


class Game:
    def __init__(self):
        pygame.init()

        # Groups:
        self.updateables = pygame.sprite.Group()
        self.drawables = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        Player.containers = (self.updateables, self.drawables)
        AsteroidField.containers = (self.updateables,)
        Asteroid.containers = (self.updateables, self.drawables, self.asteroids)
        Shot.containers = (self.updateables, self.drawables, self.shots)

        self.player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
        AsteroidField()

    def start(self):
        """Starts the game."""
        init_text()

        dt, clock = 0, pygame.time.Clock()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Game loop:
        while True:
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                return
            if not self.player.alive():
                print("Game over!")
                print(self.player.score)
                return

            screen.fill("black")
            self._update_sprites(dt=dt, visual_effects=True)
            for drawable in self.drawables:
                drawable.draw(screen=screen)

            pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")
            pygame.display.flip()
            dt = clock.tick(60) / 1000

    def sim(self, dt: float = 0.05):
        """Starts a simulation of the game - headless and sped up."""
        # Game loop:
        for i in itertools.count():
            if not self.player.alive() or any(
                event == pygame.QUIT for event in pygame.event.get()
            ):
                return i, self.player.score

            self._update_sprites(dt=dt)

    def _update_sprites(self, dt: float, visual_effects: bool = True):
        self.updateables.update(dt=dt)

        for i, asteroid in enumerate(self.asteroids):
            if asteroid.is_colliding(obj=self.player):
                points = asteroid.resolve_collision(obj=self.player) or 0
                if visual_effects:
                    explosion = Explosion(
                        position=asteroid.position, radius=asteroid.radius
                    )
                    self.updateables.add(explosion)
                    self.drawables.add(explosion)
                self.player.respawn(points_lost=points)
            for j in range(i + 1, len(self.asteroids)):
                other = self.asteroids.sprites()[j]
                if asteroid.is_colliding(other):
                    asteroid.resolve_collision(other)
            for shot in self.shots:
                if asteroid.is_colliding(obj=shot):
                    self.player.score += asteroid.split(damage=shot.damage)
                    if not asteroid.alive() and visual_effects:
                        explosion = Explosion(
                            position=asteroid.position, radius=asteroid.radius
                        )
                        self.updateables.add(explosion)
                        self.drawables.add(explosion)
                    shot.kill()


if __name__ == "__main__":
    Game().start()
