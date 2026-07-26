import pygame
import math
from Scripts.ai_base import AIBase
from Scripts.utils import has_line_of_sight, get_cover_position

class RuleBasedAI(AIBase):
    def __init__(self, npc):
        super().__init__(npc)
        self.attack_range = 80.0
        self.chase_range = 300.0
        # Safe waypoints away from obstacles
        self.patrol_points = [(100, 100), (700, 100), (700, 500), (100, 500)]
        import random
        self.current_patrol_index = random.randint(0, 3) # Spread them out
        self.attack_cooldown = 1.0
        self.time_since_last_attack = 0.0
        self.cover_target = None

    def update(self, dt, player, obstacles):
        # Update cooldowns
        self.time_since_last_attack += dt
        
        # Calculate distance to player
        dx = player.rect.centerx - self.npc.rect.centerx
        dy = player.rect.centery - self.npc.rect.centery
        distance_to_player = math.hypot(dx, dy)
        
        # Calculate Line of Sight
        player_visible = has_line_of_sight(self.npc.rect.center, player.rect.center, obstacles)
        
        # RULE-BASED LOGIC TREE
        
        # Rule 1: Retreat if health is low (< 30)
        if self.npc.health < 30:
            self.current_state = "Retreat (Cover)"
            if not self.cover_target:
                self.cover_target = get_cover_position(self.npc.rect, player.rect, obstacles)
            
            if self.cover_target:
                self.npc.move_towards(self.cover_target, dt, obstacles)
                # If we reached cover, stop moving
                if math.hypot(self.cover_target[0] - self.npc.rect.centerx, self.cover_target[1] - self.npc.rect.centery) < 10:
                    self.npc.stop_moving()
            else:
                # Fallback if no cover found
                self._retreat_from(player, dt, obstacles)
            
        # Rule 2: Seek ammo if ammo is 0
        elif self.npc.ammo <= 0:
            self.current_state = "Seeking Ammo"
            self.cover_target = None # Clear cover target
            self._patrol(dt, obstacles)
            
        # Rule 3: Attack if player is very close, we have ammo, AND we can see them
        elif distance_to_player < self.attack_range and self.npc.ammo > 0 and player_visible:
            self.current_state = "Attack"
            self.cover_target = None
            self.npc.stop_moving()
            if self.time_since_last_attack >= self.attack_cooldown:
                self._attack(player)
                self.time_since_last_attack = 0.0
                
        # Rule 4: Chase if player is visible/nearby
        elif distance_to_player < self.chase_range and player_visible:
            self.current_state = "Chase"
            self.cover_target = None
            self.npc.move_towards(player.rect.center, dt, obstacles)
            
        # Rule 5: Patrol (includes searching if they lost line of sight)
        else:
            if distance_to_player < self.chase_range and not player_visible:
                self.current_state = "Search"
            else:
                self.current_state = "Patrol"
            self.cover_target = None
            self._patrol(dt, obstacles)

    def _retreat_from(self, player, dt, obstacles):
        # Move in the opposite direction of the player
        dx = self.npc.rect.centerx - player.rect.centerx
        dy = self.npc.rect.centery - player.rect.centery
        target_pos = (self.npc.rect.centerx + dx, self.npc.rect.centery + dy)
        self.npc.move_towards(target_pos, dt, obstacles)

    def _attack(self, player):
        # Simple distance-based combat: directly deal damage
        if self.npc.ammo > 0:
            player.take_damage(10)
            self.npc.ammo -= 1.0

    def _patrol(self, dt, obstacles):
        target_pos = self.patrol_points[self.current_patrol_index]
        dx = target_pos[0] - self.npc.rect.centerx
        dy = target_pos[1] - self.npc.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance < 10:
            # Reached waypoint, go to next
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        else:
            self.npc.move_towards(target_pos, dt, obstacles)
