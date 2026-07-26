"""
settings.py - Global constants and configuration for the SmartNPC demo.
"""

# ── Window Settings ──────────────────────────────────────────────────
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576
FPS = 60
WINDOW_TITLE = "SmartNPC - Warehouse Demo"

# ── Colors (RGB) ─────────────────────────────────────────────────────
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_CARTON_OUTLINE = (205, 133, 63)   # Sandy-brown for warehouse cartons
COLOR_GOAL_ZONE = (220, 220, 220)       # Light grey for the goal/target zone
COLOR_PLAYER = (255, 255, 255)          # White triangle player

# ── Player Settings ──────────────────────────────────────────────────
PLAYER_SPEED = 4
PLAYER_SIZE = 24        # Half-height of the triangle

# ── Level Border (playable area inset from window edges) ─────────────
BORDER_MARGIN = 10

# ── Obstacle Definitions (x, y, width, height) ──────────────────────
OBSTACLES = [
    {"x": 100, "y": 150, "w": 70,  "h": 70},     # Small carton, upper-left
    {"x": 250, "y": 300, "w": 100, "h": 120},     # Medium carton, center-left
    {"x": 600, "y": 280, "w": 140, "h": 140},     # Large carton, center-right
    {"x": 820, "y": 100, "w": 110, "h": 90},      # Medium carton, upper-right
]

# ── Goal Zone (white rectangle at top-center) ───────────────────────
GOAL_ZONE = {"x": 412, "y": 15, "w": 200, "h": 30}
