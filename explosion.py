import pygame
from pygame.math import Vector2


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, radius: float, duration: float = 0.3):
        super().__init__()
        self.position = Vector2(position)
        self.radius = radius
        self.duration = duration
        self.elapsed = 0

    def update(self, dt: float):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.kill()

    def draw(self, screen: pygame.Surface):
        progress = self.elapsed / self.duration
        alpha = max(255 * (1 - progress), 0)
        current_radius = self.radius * (1 + progress * 1.5)

        surface = pygame.Surface(
            (current_radius * 2, current_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            surface,
            (255, 255, 255, int(alpha)),
            (current_radius, current_radius),
            int(current_radius),
            width=2,
        )
        screen.blit(surface, self.position - Vector2(current_radius, current_radius))
