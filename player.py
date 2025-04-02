from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED
import pygame


class Player(CircleShape):
    """TODO"""

    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y, radius=PLAYER_RADIUS)
        self.rotation = 0

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
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt=dt * -1)

        if keys[pygame.K_d]:
            self.rotate(dt=dt)

        if keys[pygame.K_w]:
            self.move(dt=dt)

        if keys[pygame.K_s]:
            self.move(dt=dt * -1)

    def move(self, dt: int):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
