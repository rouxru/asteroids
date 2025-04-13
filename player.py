import pygame

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

    def rotate(self, dt: float) -> None:
        """Rotates player."""
        self.rotation += PLAYER_TURN_SPEED * dt

        if self.rotation < 0:
            self.rotation += 360
        elif self.rotation > 360:
            self.rotation -= 360

    def update(self, dt: float) -> None:
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

    def move(self, dt: float) -> None:
        """Moves player."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        next_x, next_y = self.position + forward * PLAYER_SPEED * dt

        if next_x < 0:
            next_x = SCREEN_WIDTH
        elif next_x > SCREEN_WIDTH:
            next_x -= SCREEN_WIDTH

        if next_y < 0:
            next_y = SCREEN_HEIGHT
        elif next_y > SCREEN_HEIGHT:
            next_y -= SCREEN_HEIGHT

        self.position = pygame.Vector2(next_x, next_y)

    def shoot(self) -> None:
        """Shoots gun."""
        if self.shot_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y, damage=PRIMARY_WEOPON_DAMAGE)  # type: ignore
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN

    def respawn(self, points_lost: float) -> None:
        """Respawns player and takes away points based on asteroid."""
        self.lives -= 1
        if not self.lives:
            return self.kill()

        self.score = max(0, self.score - points_lost)

    def kill(self):
        """Print current player score and kill."""
        return super().kill()
