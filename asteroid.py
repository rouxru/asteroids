from typing import Optional
from circleshape import CircleShape
import pygame
import random
from constants import (
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from debris import DebrisParticle
from math import radians, sin, cos


class Asteroid(CircleShape):
    """Asteroid class."""

    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x=x, y=y, radius=radius)
        self.health_points = self.radius
        self.shape_points = self.generate_shape_points()
        self.rotation_angle = 0
        self.rotation_speed = random.uniform(-40, 40)

    def generate_shape_points(self, spikiness=0.3, num_vertices=16):
        """Generates edged shape to better represent an asteroid."""
        angle_step = 360 / num_vertices
        points = []

        for i in range(num_vertices):
            angle_deg = i * angle_step
            angle_rad = radians(angle_deg)
            reduction = random.uniform(0, spikiness * self.radius)
            rad = max(2, self.radius - reduction)

            x = rad * cos(angle_rad)
            y = rad * sin(angle_rad)
            points.append((x, y))

        return points

    def draw(self, screen: "pygame.Surface") -> None:
        """Draws asteroid."""
        angle_rad = radians(self.rotation_angle)
        cos_a = cos(angle_rad)
        sin_a = sin(angle_rad)

        rotated = []
        for point in self.shape_points:
            dx, dy = point
            rx = dx * cos_a - dy * sin_a
            ry = dx * sin_a + dy * cos_a
            rotated.append((self.position.x + rx, self.position.y + ry))  # type: ignore

        pygame.draw.polygon(screen, "white", rotated, width=2)

    def get_rotated_points(self):
        """Calculate rotating points."""
        rotated = []
        angle_rad = radians(self.rotation_angle)
        cos_a = cos(angle_rad)
        sin_a = sin(angle_rad)

        for point in self.shape_points:
            dx = point[0] - self.position.x  # type: ignore
            dy = point[1] - self.position.y  # type: ignore

            rx = dx * cos_a - dy * sin_a
            ry = dx * sin_a + dy * cos_a

            rotated.append((self.position.x + rx, self.position.y + ry))  # type: ignore

        return rotated

    def update(self, dt: int) -> None:
        """Called every frame."""
        self.position += self.velocity * dt  # type: ignore
        self.rotation_angle += self.rotation_speed * dt
        self.rotation_angle %= 360

        margin = ASTEROID_MAX_RADIUS * 2
        if (
            self.position.x < -margin
            or self.position.x > SCREEN_WIDTH + margin
            or self.position.y < -margin
            or self.position.y > SCREEN_HEIGHT + margin
        ):
            self.kill()

    def split(self, damage: float) -> int:
        """Splits asteroid if its not the smallest, otherwise kills it."""
        self.health_points -= damage

        if hasattr(self, "containers"):
            updateables, drawables, _ = self.containers  # type: ignore
            self.generate_debris_effects(drawables, updateables)

        if self.health_points <= 0:
            self.kill()
            if self.radius <= ASTEROID_MIN_RADIUS:
                return self.get_points_for_kill()
            else:
                v1 = self.velocity.rotate(random.uniform(20, 50))  # type: ignore
                v2 = self.velocity.rotate(random.uniform(-20, -50))  # type: ignore
                new_rad = self.radius - ASTEROID_MIN_RADIUS
                smaller_asteroid_one = Asteroid(
                    x=self.position.x, y=self.position.y, radius=new_rad  # type: ignore
                )
                smaller_asteroid_one.velocity = v1 * 1.2
                smaller_asteroid_two = Asteroid(
                    x=self.position.x, y=self.position.y, radius=new_rad  # type: ignore
                )
                smaller_asteroid_two.velocity = v2 * 1.2
                return self.get_points_for_kill() - self.radius / 2
        return 0

    def get_points_for_kill(self) -> int:
        """Returns how many points this asteroid is worth."""
        return self.radius * 1.5

    def generate_debris_effects(self, drawables, updateables) -> None:
        """Generates effect when being shot."""
        num_particles = random.randint(2, 4)
        for _ in range(num_particles):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 150)
            vel = (
                self.velocity.rotate(angle) + pygame.Vector2(1, 0).rotate(angle) * speed  # type: ignore
            )
            particle = DebrisParticle(
                position=self.position, velocity=vel, radius=self.radius * 0.2
            )
            updateables.add(particle)
            drawables.add(particle)

    def resolve_collision(self, obj) -> Optional[float]:
        """Resolves collision of asteroid with other objects in the field."""
        from player import Player

        if isinstance(obj, Player):
            if self.alive() and obj.alive():
                points = self.get_points_for_kill() / 2
                self.kill()
                return points

        elif isinstance(obj, Asteroid) and obj != self:
            if self.alive() and obj.alive():
                delta = self.position - obj.position
                distance = delta.length()

                if distance == 0:
                    return

                normal = delta.normalize()
                rel_vel = self.velocity - obj.velocity
                vel_along_normal = rel_vel.dot(normal)

                if vel_along_normal > 0:
                    return

                self.velocity -= normal * vel_along_normal
                obj.velocity += normal * vel_along_normal

                overlap = (self.radius + obj.radius) - distance
                if overlap > 0:
                    correction = normal * (overlap / 2)
                    self.position += correction
                    obj.position -= correction
