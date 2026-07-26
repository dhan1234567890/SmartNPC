"""
game.py - Core game loop: initialises Pygame, runs the update/draw cycle.
"""

# pyrefly: ignore [missing-import]
import pygame
import sys
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE
from src.player import Player
from src.level import Level


class Game:
    """Top-level game controller."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.level = Level()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.level.obstacle_rects)

    def _draw(self):
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()
