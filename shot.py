from circleshape import CircleShape
import pygame
from constants import SHOT_RADIUS


class Shot(CircleShape):

    def __init__(self, x: float, y: float, damage: float):
        super().__init__(x=x, y=y, radius=SHOT_RADIUS)
        self.damage = damage

    def draw(self, screen: "pygame.Surface") -> None:
        """TODO"""
        pygame.draw.circle(
            surface=screen,
            color="yellow",
            center=self.position,
            radius=self.radius,
            width=2,
        )

    def update(self, dt: int) -> None:
        """TODO"""
        self.position += self.velocity * dt
