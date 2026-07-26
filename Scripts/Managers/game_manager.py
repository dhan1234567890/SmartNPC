import pygame
import random
from Scripts.Player.player import Player
from Scripts.NPC.npc import BaseNPC
from Scripts.RuleBasedAI.rule_based import RuleBasedAI
from Scripts.pickup import Pickup

class GameManager:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        # Increase width by 200 for the dashboard UI
        self.ui_width = 250
        self.screen = pygame.display.set_mode((self.screen_width + self.ui_width, self.screen_height))
        pygame.display.set_caption("Fuzzy Logic Decision NPCs")
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 14)
        self.title_font = pygame.font.SysFont('Arial', 18, bold=True)
        
        self.bg_color = (30, 30, 30)
        self.ui_color = (20, 20, 20)
        
        self.player = Player(100, 100)
        
        # Phase 2: Rule-Based NPCs
        self.npcs = [
            BaseNPC(100, 500),
            BaseNPC(600, 100),
            BaseNPC(600, 400)
        ]
        
        # Active AI controllers
        self.ai_type = "Rule-Based"
        self.ai_controllers = [RuleBasedAI(npc) for npc in self.npcs]
        
        # Simple obstacles to provide cover
        self.obstacles = [
            pygame.Rect(300, 200, 200, 50),
            pygame.Rect(300, 400, 200, 50),
            pygame.Rect(150, 300, 50, 150),
            pygame.Rect(600, 150, 50, 150)
        ]
        
        self.pickups = []
        self.pickup_spawn_timer = 0.0

        self.game_over = False
        self.win = False
        self.game_over_font = pygame.font.SysFont('Arial', 48, bold=True)

    def update(self, dt, mouse_clicked = False):
        if self.game_over:
            return

        # AI Swapping via Keys 1, 2, 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.ai_type = "Rule-Based"
            self.ai_controllers = [RuleBasedAI(npc) for npc in self.npcs]
        # elif keys[pygame.K_2]:
        #     self.ai_type = "FSM"
        #     self.ai_controllers = [FSMAI(npc) for npc in self.npcs]
        # elif keys[pygame.K_3]:
        #     self.ai_type = "Fuzzy Logic"
        #     self.ai_controllers = [FuzzyLogicAI(npc) for npc in self.npcs]

        # Spawn Pickups randomly
        self.pickup_spawn_timer += dt
        if self.pickup_spawn_timer > 5.0: # spawn every 5 seconds
            self.pickup_spawn_timer = 0.0
            if len(self.pickups) < 5:
                type_p = random.choice(["health", "ammo"])
                x = random.randint(50, self.screen_width - 50)
                y = random.randint(50, self.screen_height - 50)
                self.pickups.append(Pickup(x, y, type_p))

        # Update player
        self.player.update(dt, self.screen_width, self.screen_height, self.obstacles, self.npcs, self.pickups, mouse_clicked=mouse_clicked)
        
        # Check player death
        if self.player.health <= 0:
            self.game_over = True
        
        # Update AI Logic
        for ai in self.ai_controllers:
            ai.update(dt, self.player, self.obstacles)
            
        # Update NPCs physical movement/state
        for npc in self.npcs:
            npc.update(dt, self.player, self.obstacles, self.pickups, self.screen_width, self.screen_height)
            
        # Remove dead NPCs (Health <= 0)
        alive_npcs = []
        alive_ai = []
        for i, npc in enumerate(self.npcs):
            if npc.health > 0:
                alive_npcs.append(npc)
                alive_ai.append(self.ai_controllers[i])
        
        self.npcs = alive_npcs
        self.ai_controllers = alive_ai

        #check win condition
        if len(self.npcs) == 0 and not self.game_over:
            self.game_over = True
            self.win = True

    def draw(self):
        # Draw game area
        self.screen.fill(self.bg_color, (0, 0, self.screen_width, self.screen_height))
        
        if self.game_over:
            if self.win:
                msg, color = "YOU WIN!", (0, 255, 100)
            else:
                msg, color = "GAME OVER", (255, 0, 0)

            go_text = self.game_over_font.render(msg, True, color)
            self.screen.blit(go_text, (self.screen_width // 2 - go_text.get_width() // 2, self.screen_height // 2 - go_text.get_height() // 2))
        else:
            # Draw Pickups
            for pickup in self.pickups:
                pickup.draw(self.screen)
            
            # Draw obstacles
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, (100, 100, 100), obs)
                
            # Draw NPCs and state text
            for i, npc in enumerate(self.npcs):
                npc.draw(self.screen)
                state = self.ai_controllers[i].current_state
                text_surface = self.font.render(f"[{state}]", True, (255, 255, 255))
                self.screen.blit(text_surface, (npc.rect.centerx - text_surface.get_width()//2, npc.rect.y - 25))
                
            # Draw player
            self.player.draw(self.screen)
        
        # Draw UI Dashboard
        self._draw_dashboard()
        
        pygame.display.flip()
        
    def _draw_dashboard(self):
        # Background
        ui_rect = pygame.Rect(self.screen_width, 0, self.ui_width, self.screen_height)
        pygame.draw.rect(self.screen, self.ui_color, ui_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (self.screen_width, 0), (self.screen_width, self.screen_height), 2)
        
        # Title
        title = self.title_font.render("AI Dashboard", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width + 10, 10))
        
        # Controls
        controls = self.font.render("Controls:", True, (200, 200, 200))
        self.screen.blit(controls, (self.screen_width + 10, 40))
        ctrl_text = self.font.render("[1] Rule-Based  [LMB/SPC] Attack", True, (150, 150, 150))
        self.screen.blit(ctrl_text, (self.screen_width + 10, 60))
        
        # AI State``
        ai_title = self.title_font.render(f"Active AI: {self.ai_type}", True, (100, 200, 255))
        self.screen.blit(ai_title, (self.screen_width + 10, 100))
        
        # NPC Stats
        if self.npcs and self.ai_controllers:
            y_offset = 130
            for i, (npc, ai) in enumerate(zip(self.npcs, self.ai_controllers)):
                title_text = self.font.render(f"--- NPC {i+1} ---", True, (200, 200, 200))
                self.screen.blit(title_text, (self.screen_width + 10, y_offset))
                y_offset += 20
                
                stats = [
                    f"Health: {int(npc.health)}",
                    f"Ammo: {int(npc.ammo)}",
                    f"State: {ai.current_state}"
                ]
                for stat in stats:
                    text = self.font.render(stat, True, (255, 255, 255))
                    self.screen.blit(text, (self.screen_width + 10, y_offset))
                    y_offset += 18
                
                y_offset += 10 # spacing between NPCs
                
        # Player Stats (For Debug)
        p_stats = self.title_font.render("Player Stats", True, (100, 255, 100))
        self.screen.blit(p_stats, (self.screen_width + 10, 420))
        p_health = self.font.render(f"Health: {int(self.player.health)}", True, (255, 255, 255))
        self.screen.blit(p_health, (self.screen_width + 10, 445))
        p_ammo = self.font.render(f"Ammo: {int(self.player.ammo)}", True, (255, 255, 255))
        self.screen.blit(p_ammo, (self.screen_width + 10, 465))
        
