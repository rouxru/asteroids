import pygame
from pygame.math import Vector2


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, radius: float, duration: float = 0.3):
        super().__init__()
        self.position = Vector2(position)
        self.radius = radius
        self.duration = duration
        self.elapsed = 0

        size = int((radius * 2) * 2.5)
        self.base_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(
            self.base_surface,
            (255, 255, 255, 255),
            (size // 2, size // 2),
            int(radius),
            width=2,
        )

        self.size = size

    def update(self, dt: float):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.kill()

    def draw(self, screen: pygame.Surface):
        progress = self.elapsed / self.duration
        alpha = max(255 * (1 - progress), 0)
        scale = 1 + progress * 1.5
        scaled_size = int(self.size * scale)

        surface = pygame.transform.smoothscale(
            self.base_surface, (scaled_size, scaled_size)
        )
        surface.set_alpha(int(alpha))

        screen.blit(surface, self.position - Vector2(scaled_size / 2, scaled_size / 2))
