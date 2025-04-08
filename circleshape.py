import pygame


class CircleShape(pygame.sprite.Sprite):
    """Base class for game objects."""

    containers: tuple["pygame.sprite.Group", ...]

    def __init__(self, *groups, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(*self.containers, *groups)
        else:
            super().__init__(*groups)

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: "pygame.Surface") -> None:
        """Sub-classes must override"""
        pass

    def update(self, dt: int) -> None:
        """Sub-classes must override"""
        pass

    def is_colliding(self, obj: "CircleShape") -> bool:
        """Is this object colliding with another."""
        return self.position.distance_to(obj.position) <= self.radius + obj.radius
