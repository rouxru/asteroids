import pygame
from constants import *
from utils import init_text
from player import Player


def main():
    init_text()
    pygame.init()
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        player.update(dt=dt)
        player.draw(screen=screen)
        pygame.display.flip()
        dt = clock.tick() / 1000


if __name__ == "__main__":
    main()
