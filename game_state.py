"""Capture game state and player actions."""

import dataclasses
import math
from typing import TYPE_CHECKING, Optional

import pygame

if TYPE_CHECKING:
    from asteroid import Asteroid
    from circleshape import CircleShape
    from main import Game
    from player import Player


@dataclasses.dataclass
class GameState:
    """Describes game state at a givent moment in a way the ship AI can understand."""

    ship_angle: float
    """Ship's angle (rotation)."""

    asteroid_dist: float
    """Distance from the ship to the nearest asteroid."""

    asteroid_angle: float
    """Angle between the ship and the nearest asteroid."""

    asteroid_relative_velocity: "pygame.Vector2"
    """Relative velocity of the nearest asteroid to the ship. (asteroid's vector - ship's vector)"""

    pressed_keys: list[int]
    """Keys pressed by the player, e.g. `pygame.K_w` == 119."""


def get_game_state(game: "Game") -> Optional["GameState"]:
    ship = game.player
    if not game.asteroids:
        return

    asteroid, dist = get_nearest_asteroid(ship=ship, asteroids=game.asteroids.sprites())
    ship_angle = round(ship.rotation, 3)
    asteroid_relative_velocity = asteroid.velocity - ship.velocity
    asteroid_relative_velocity.x = round(asteroid_relative_velocity.x, 3)
    asteroid_relative_velocity.y = round(asteroid_relative_velocity.y, 3)

    # get the angle between the ship and the asteroid
    dx = ship.position.x - asteroid.position.x
    dy = ship.position.y - asteroid.position.y
    angle_to_target = math.degrees(math.atan2(dy, dx))
    angle_difference = (angle_to_target - ship.rotation) % 360

    return GameState(
        ship_angle=ship_angle,
        asteroid_dist=dist,
        asteroid_angle=angle_difference,
        asteroid_relative_velocity=asteroid_relative_velocity,
        pressed_keys=get_pressed_keys(),
    )


def get_nearest_asteroid(
    ship: "Player", asteroids: list["Asteroid"]
) -> tuple["Asteroid", float]:
    def dist(a: "CircleShape", b: "CircleShape") -> float:
        return round(
            math.hypot(a.position.x - b.position.x, a.position.y - b.position.y), 3
        )

    _min_asteroid, _min_dist = asteroids[0], dist(ship, asteroids[0])

    for a in asteroids[1:]:
        d = dist(ship, a)
        if d < _min_dist:
            _min_dist = d
            _min_asteroid = a

    return _min_asteroid, _min_dist


def get_pressed_keys() -> list[int]:
    """Returns the currently pressed keys."""
    valid_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE]
    pressed_keys = pygame.key.get_pressed()
    return [key for key in valid_keys if pressed_keys[key]]
