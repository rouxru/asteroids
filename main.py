import pygame
from constants import *
from utils import init_text
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion


def main():
    init_text()
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Groups:
    updateables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids: list["Asteroid"] = pygame.sprite.Group()  # type: ignore
    shots: list["Shot"] = pygame.sprite.Group()  # type: ignore

    Player.containers = (updateables, drawables)  # type: ignore
    Asteroid.containers = (updateables, drawables, asteroids)  # type: ignore
    AsteroidField.containers = (updateables,)  # type: ignore
    Shot.containers = (updateables, drawables, shots)  # type: ignore

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Game loop:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updateables.update(dt=dt)

        for i, asteroid in enumerate(asteroids):
            if asteroid.is_colliding(obj=player):
                points = asteroid.resolve_collision(obj=player) or 0
                explosion = Explosion(
                    position=asteroid.position, radius=asteroid.radius
                )
                updateables.add(explosion)
                drawables.add(explosion)
                player.respawn(points_lost=points)
            for j in range(i + 1, len(asteroids)):
                other = asteroids.sprites()[j]  # type: ignore
                if asteroid.is_colliding(other):
                    asteroid.resolve_collision(other)

            for shot in shots:
                if asteroid.is_colliding(obj=shot):
                    player.score += asteroid.split(damage=shot.damage)
                    if not asteroid.alive():
                        explosion = Explosion(
                            position=asteroid.position, radius=asteroid.radius
                        )
                        updateables.add(explosion)
                        drawables.add(explosion)
                    shot.kill()

        if not player.alive():
            print("Game over!")
            return

        for drawable in drawables:
            drawable.draw(screen=screen)

        pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
