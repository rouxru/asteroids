import itertools
from typing import TYPE_CHECKING, Optional

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from explosion import Explosion
from player import Player
from shot import Shot
from utils import init_text, is_colliding

if TYPE_CHECKING:
    from ai.nn import NeuralNetwork


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

    def start(self, ship_ai: Optional["NeuralNetwork"] = None):
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

            if ship_ai:
                self.ai_move(ship_ai, dt=dt)

            screen.fill("black")
            self._update_sprites(dt=dt, visual_effects=True)
            for drawable in self.drawables:
                drawable.draw(screen=screen)

            pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")
            pygame.display.flip()
            dt = clock.tick(60) / 1000

    def sim(self, ship_ai: "NeuralNetwork", dt: float = 0.05) -> tuple[int, float]:
        """Starts a simulation of the game - headless and sped up."""
        from collections import Counter

        taken_actions = Counter()

        # Game loop:
        for i in itertools.count():
            if not self.player.alive() or any(
                event.type == pygame.QUIT for event in pygame.event.get()
            ):
                # punish the ships that are not using all outputs
                if len(taken_actions) < 4:
                    return 0, 0
                return i, self.player.score

            action = self.ai_move(ship_ai, dt=dt)
            taken_actions[action] += 1
            self._update_sprites(dt=dt)

        raise RuntimeError("needed for typehint")

    def ai_move(self, ship_ai: "NeuralNetwork", dt: float) -> Optional[int]:
        """The AI makes a move based on current game state."""
        from game_state import get_game_state

        if self.asteroids.sprites():
            game_state = get_game_state(self)
            if not game_state:
                return

            ai_action = int(ship_ai.predict(game_state))  # 0, 1, 2, 3

            if ai_action == 0:
                self.player.move(dt=dt)
            if ai_action == 1:
                self.player.rotate(dt=dt)
            if ai_action == 2:
                self.player.rotate(dt=dt)
            if ai_action == 3:
                self.player.shoot()

            return ai_action

    def _update_sprites(self, dt: float, visual_effects: bool = True):
        self.updateables.update(dt=dt)

        for i, asteroid in enumerate(self.asteroids):
            if is_colliding(asteroid, self.player):
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
                if is_colliding(asteroid, other):
                    asteroid.resolve_collision(other)
            for shot in self.shots:
                if is_colliding(asteroid, shot):
                    self.player.score += asteroid.split(damage=shot.damage)
                    if not asteroid.alive() and visual_effects:
                        explosion = Explosion(
                            position=asteroid.position, radius=asteroid.radius
                        )
                        self.updateables.add(explosion)
                        self.drawables.add(explosion)
                    shot.kill()

    def load_ai(self):
        """Loads an AI into the game and starts it."""
        import pickle

        from ai.genetic_gym import SAVE_PATH

        with open(SAVE_PATH, "rb") as f:
            ship_ai = pickle.load(f)

        self.start(ship_ai=ship_ai)


if __name__ == "__main__":
    Game().start()

    # to start an AI game:
    # Game().load_ai()
