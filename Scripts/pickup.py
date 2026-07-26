import pygame

class Pickup:
    def __init__(self, x, y, pickup_type):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.pickup_type = pickup_type # "health" or "ammo"
        
        if self.pickup_type == "health":
            self.color = (0, 255, 0) # Green
            self.amount = 25.0
        else:
            self.color = (255, 255, 0) # Yellow
            self.amount = 10.0
            
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1) # Small outline
