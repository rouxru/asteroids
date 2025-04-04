from circleshape import CircleShape
from constants import (
    PLAYER_LIVES,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PRIMARY_WEOPON_DAMAGE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
import pygame
from shot import Shot


class Player(CircleShape):
    """Player class."""

    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y, radius=PLAYER_RADIUS)
        self.lives = PLAYER_LIVES
        self.rotation = 0
        self.shot_timer = 0
        self.score = 0

    def triangle(self) -> list:
        """Generates players drawn shape."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: "pygame.Surface"):
        """Draws player."""
        pygame.draw.polygon(
            surface=screen, color="white", points=self.triangle(), width=2
        )

    def rotate(self, dt: int) -> None:
        """Rotates player."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: int) -> None:
        """Called every frame to track keypresses for actions."""
        self.shot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt=dt * -1)

        if keys[pygame.K_d]:
            self.rotate(dt=dt)

        if keys[pygame.K_w]:
            self.move(dt=dt)

        if keys[pygame.K_s]:
            self.move(dt=dt * -1)

        if keys[pygame.K_SPACE]:
            self.shoot()

        if (
            self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()

    def move(self, dt: int) -> None:
        """Moves player."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self) -> None:
        """Shoots gun."""
        if self.shot_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y, damage=PRIMARY_WEOPON_DAMAGE)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN

    def respawn(self, points_lost: float) -> None:
        """Respawns player and takes away points based on asteroid."""
        self.lives -= 1
        if not self.lives:
            return self.kill()

        self.score -= points_lost

    def kill(self):
        """Print current player score and kill."""
        print(f"Score: {self.score}")
        return super().kill()
