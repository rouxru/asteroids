import pygame
from pygame.math import Vector2


class DebrisParticle(pygame.sprite.Sprite):
    def __init__(
        self, position: Vector2, velocity: Vector2, radius: float, duration: float = 0.4
    ):
        super().__init__()
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.radius = radius
        self.duration = duration
        self.elapsed = 0

    def update(self, dt: float):
        self.elapsed += dt
        self.position += self.velocity * dt
        if self.elapsed >= self.duration:
            self.kill()

    def draw(self, screen: pygame.Surface):
        progress = self.elapsed / self.duration
        alpha = max(255 * (1 - progress), 0)

        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            surface,
            (200, 200, 200, int(alpha)),
            (self.radius, self.radius),
            int(self.radius),
        )
        screen.blit(surface, self.position - Vector2(self.radius, self.radius))
