"""
level.py - Level manager: draws the arena, obstacles, and goal zone.
"""

# pyrefly: ignore [missing-import]
import pygame
from src.settings import (
    COLOR_BLACK, COLOR_CARTON_OUTLINE, COLOR_GOAL_ZONE,
    SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_MARGIN,
    OBSTACLES, GOAL_ZONE,
)


class Level:
    """Manages and renders the warehouse arena layout."""

    def __init__(self):
        self.obstacle_rects: list[pygame.Rect] = [
            pygame.Rect(o["x"], o["y"], o["w"], o["h"]) for o in OBSTACLES
        ]
        self.goal_rect = pygame.Rect(
            GOAL_ZONE["x"], GOAL_ZONE["y"],
            GOAL_ZONE["w"], GOAL_ZONE["h"],
        )

    # ── draw ─────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface):
        """Render the entire level onto the surface."""
        surface.fill(COLOR_BLACK)

        # Level border
        border_rect = pygame.Rect(
            BORDER_MARGIN, BORDER_MARGIN,
            SCREEN_WIDTH - 2 * BORDER_MARGIN,
            SCREEN_HEIGHT - 2 * BORDER_MARGIN,
        )
        pygame.draw.rect(surface, (60, 60, 60), border_rect, width=1)

        # Goal zone
        pygame.draw.rect(surface, COLOR_GOAL_ZONE, self.goal_rect)

        # Carton obstacles
        for rect in self.obstacle_rects:
            pygame.draw.rect(surface, COLOR_CARTON_OUTLINE, rect, width=3)
