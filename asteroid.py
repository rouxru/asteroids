from circleshape import CircleShape
import pygame


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x=x, y=y, radius=radius)

    def draw(self, screen: "pygame.Surface") -> None:
        pygame.draw.circle(
            surface=screen,
            color="white",
            center=self.position,
            radius=self.radius,
            width=2,
        )

    def update(self, dt: int) -> None:
        self.position += self.velocity * dt
