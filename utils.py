from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from circleshape import CircleShape


def init_text():
    """Utility function to print initial game launch params."""
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


def is_colliding(obj_one: "CircleShape", obj_two: "CircleShape") -> bool:
    """Utility function to determine if two objects are colliding."""
    return (
        obj_one.position.distance_to(obj_two.position)
        <= obj_one.radius + obj_two.radius
    )
