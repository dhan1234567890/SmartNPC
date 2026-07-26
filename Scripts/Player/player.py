import pygame
import math

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (0, 128, 255) # Blue
        self.speed = 200
        
        self.health = 100.0
        self.ammo = 15.0
        self.attack_range = 90.0
        self.time_since_last_attack = 0.0
        self.attack_cooldown = 0.5
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def update(self, dt, screen_width, screen_height, obstacles, npcs, pickups, mouse_clicked = False):
        self.time_since_last_attack += dt
        keys = pygame.key.get_pressed()
        
        # Handle movement
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
            
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
            
        move_x = dx * self.speed * dt
        move_y = dy * self.speed * dt
        
        # Horizontal movement & collision
        self.rect.x += move_x
        self._handle_collisions(obstacles, 'x')
        
        # Vertical movement & collision
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
        
        # Handle attack
        if (mouse_clicked or keys[pygame.K_SPACE]) and self.time_since_last_attack >= self.attack_cooldown and self.ammo > 0:
            self._attack(npcs, obstacles)
            
    def _attack(self, npcs, obstacles):
        from Scripts.utils import has_line_of_sight
        attacked = False
        for npc in npcs:
            dx = npc.rect.centerx - self.rect.centerx
            dy = npc.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist <= self.attack_range and has_line_of_sight(self.rect.center, npc.rect.center, obstacles):
                npc.take_damage(20) # Player deals 20 damage per hit
                attacked = True
        
        if attacked:
            self.ammo -= 1.0
            self.time_since_last_attack = 0.0

    def _handle_collisions(self, obstacles, axis):
        for obs in obstacles:
            if self.rect.colliderect(obs):
                if axis == 'x':
                    if self.rect.right > obs.left and self.rect.left < obs.left:
                        self.rect.right = obs.left
                    elif self.rect.left < obs.right and self.rect.right > obs.right:
                        self.rect.left = obs.right
                elif axis == 'y':
                    if self.rect.bottom > obs.top and self.rect.top < obs.top:
                        self.rect.bottom = obs.top
                    elif self.rect.top < obs.bottom and self.rect.bottom > obs.bottom:
                        self.rect.top = obs.bottom

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2) # Outline
        
        # Draw player health bar
        health_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100.0), 5)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)
        
        # Draw attack range indicator (optional, useful for debugging/testing)
        pygame.draw.circle(surface, (255, 255, 255), self.rect.center, int(self.attack_range), 1)

