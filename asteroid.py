from circleshape import CircleShape
import pygame
import random
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x=x, y=y, radius=radius)
        self.health_points = self.radius

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

    def split(self, damage: float) -> None:
        self.health_points -= damage
        if self.health_points <= 0:
            self.kill()
            if self.radius <= ASTEROID_MIN_RADIUS:
                return
            else:
                v1 = self.velocity.rotate(random.uniform(20, 50))
                v2 = self.velocity.rotate(random.uniform(-20, -50))
                new_rad = self.radius - ASTEROID_MIN_RADIUS
                smaller_asteroid_one = Asteroid(
                    x=self.position.x, y=self.position.y, radius=new_rad
                )
                smaller_asteroid_one.velocity = v1 * 1.2
                smaller_asteroid_two = Asteroid(
                    x=self.position.x, y=self.position.y, radius=new_rad
                )
                smaller_asteroid_two.velocity = v2 * 1.2
