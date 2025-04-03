from circleshape import CircleShape
import pygame
import pygame.math
import random
from constants import ASTEROID_MIN_RADIUS
from debris import DebrisParticle


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

    def split(self, damage: float) -> int:
        self.health_points -= damage

        if hasattr(self, "containers"):
            updateables, drawables, _ = self.containers
            self.generate_debris_effects(drawables, updateables)

        if self.health_points <= 0:
            self.kill()
            if self.radius <= ASTEROID_MIN_RADIUS:
                return self.get_points_for_kill()
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
                return self.get_points_for_kill() - self.radius / 2
        return 0

    def get_points_for_kill(self) -> int:
        return self.radius * 1.5

    def generate_debris_effects(self, drawables, updateables) -> None:
        num_particles = random.randint(2, 4)
        for _ in range(num_particles):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 150)
            vel = (
                self.velocity.rotate(angle) + pygame.Vector2(1, 0).rotate(angle) * speed
            )
            particle = DebrisParticle(
                position=self.position, velocity=vel, radius=self.radius * 0.2
            )
            updateables.add(particle)
            drawables.add(particle)
