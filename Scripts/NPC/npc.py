import pygame
import math

class BaseNPC:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (255, 64, 64) # Red
        
        # Basic state variables for future AI control
        self.health = 100.0
        self.ammo = 10.0
        self.speed = 100.0
        
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        
        # Current action target
        self.target_position = None

    def move_towards(self, target_pos, dt, obstacles):
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            self.velocity_x = (dx / dist) * self.speed
            self.velocity_y = (dy / dist) * self.speed
        else:
            self.stop_moving()

    def stop_moving(self):
        self.velocity_x = 0
        self.velocity_y = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def update(self, dt, player, obstacles, pickups, screen_width, screen_height):
        # Apply velocity
        move_x = self.velocity_x * dt
        move_y = self.velocity_y * dt
        
        self.rect.x += move_x
        self._handle_collisions(obstacles, 'x')
        
        self.rect.y += move_y
        self._handle_collisions(obstacles, 'y')
        
        # Screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(screen_height, self.rect.bottom)
        
        # Handle Pickups
        for pickup in pickups[:]:
            if self.rect.colliderect(pickup.rect):
                if pickup.pickup_type == "health":
                    self.health = min(100.0, self.health + pickup.amount)
                elif pickup.pickup_type == "ammo":
                    self.ammo = min(15.0, self.ammo + pickup.amount)
                pickups.remove(pickup)

    def _handle_collisions(self, obstacles, axis):
        for obs in obstacles:
            if self.rect.colliderect(obs):
                if axis == 'x':
                    if self.velocity_x > 0:
                        self.rect.right = obs.left
                    elif self.velocity_x < 0:
                        self.rect.left = obs.right
                elif axis == 'y':
                    if self.velocity_y > 0:
                        self.rect.bottom = obs.top
                    elif self.velocity_y < 0:
                        self.rect.top = obs.bottom

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2) # Outline
        
        # Draw basic health bar
        health_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100.0), 5)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)

