"""
player.py - Player sprite class (white triangle controlled via WASD).
"""

import pygame
from src.settings import (
    COLOR_PLAYER, PLAYER_SPEED, PLAYER_SIZE,
    SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_MARGIN,
)


class Player:
    """A white triangle the user moves with W/A/S/D keys."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.speed = PLAYER_SPEED
        self.size = PLAYER_SIZE  # half-height of the triangle

    # ── geometry helpers ─────────────────────────────────────────────
    def _get_triangle_points(self):
        """Return the three vertices of the triangle (pointing upward)."""
        return [
            (self.x, self.y - self.size),               # top vertex
            (self.x - self.size, self.y + self.size),    # bottom-left
            (self.x + self.size, self.y + self.size),    # bottom-right
        ]

    def get_rect(self) -> pygame.Rect:
        """Axis-aligned bounding box used for collision checks."""
        return pygame.Rect(
            self.x - self.size,
            self.y - self.size,
            self.size * 2,
            self.size * 2,
        )

    # ── update ───────────────────────────────────────────────────────
    def update(self, keys, obstacles: list[pygame.Rect]):
        """Move based on held keys, then clamp to borders & resolve collisions."""
        dx, dy = 0, 0

        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        # ── Move on X axis, then resolve X collisions ────────────────
        self.x += dx
        self._clamp_to_borders()
        player_rect = self.get_rect()
        for obs in obstacles:
            if player_rect.colliderect(obs):
                if dx > 0:  # moving right
                    self.x = obs.left - self.size
                elif dx < 0:  # moving left
                    self.x = obs.right + self.size

        # ── Move on Y axis, then resolve Y collisions ────────────────
        self.y += dy
        self._clamp_to_borders()
        player_rect = self.get_rect()
        for obs in obstacles:
            if player_rect.colliderect(obs):
                if dy > 0:  # moving down
                    self.y = obs.top - self.size
                elif dy < 0:  # moving up
                    self.y = obs.bottom + self.size

    def _clamp_to_borders(self):
        """Keep the player within the playable level boundaries."""
        self.x = max(BORDER_MARGIN + self.size,
                     min(self.x, SCREEN_WIDTH - BORDER_MARGIN - self.size))
        self.y = max(BORDER_MARGIN + self.size,
                     min(self.y, SCREEN_HEIGHT - BORDER_MARGIN - self.size))

    # ── draw ─────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface):
        """Render the triangle onto the given surface."""
        pygame.draw.polygon(surface, COLOR_PLAYER, self._get_triangle_points())
