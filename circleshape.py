import pygame


class CircleShape(pygame.sprite.Sprite):
    """Base class for game objects."""

    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # type: ignore
        else:
            super().__init__()

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
