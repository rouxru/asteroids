from circleshape import CircleShape
from constants import (
    PLAYER_LIVES,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PRIMARY_WEOPON_DAMAGE,
)
import pygame
from shot import Shot
from asteroid import Asteroid


class Player(CircleShape):
    """TODO"""

    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y, radius=PLAYER_RADIUS)
        self.lives = PLAYER_LIVES
        self.rotation = 0
        self.shot_timer = 0
        self.score = 0

    def triangle(self) -> list:
        """TODO"""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: "pygame.Surface"):
        """TODO"""
        pygame.draw.polygon(
            surface=screen, color="white", points=self.triangle(), width=2
        )

    def rotate(self, dt: int) -> None:
        """TODO"""
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: int) -> None:
        """TODO"""
        self.shot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt=dt * -1)

        if keys[pygame.K_d]:
            self.rotate(dt=dt)

        if keys[pygame.K_w]:
            self.move(dt=dt)

        if keys[pygame.K_s]:
            self.move(dt=dt * -1)

        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt: int) -> None:
        """TODO"""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self) -> None:
        """TODO"""
        if self.shot_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y, damage=PRIMARY_WEOPON_DAMAGE)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN

    def respawn(self, asteroid: "Asteroid") -> None:
        """TODO"""
        if self.lives - 1 == 0:
            self.kill()
            return

        self.lives -= 1
        asteroid.kill()
        self.score -= asteroid.get_points_for_kill() / 2
