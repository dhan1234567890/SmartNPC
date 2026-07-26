import pygame
import sys
from Scripts.Managers.game_manager import GameManager

def main():
    pygame.init()
    
    # Initialize game manager
    game_manager = GameManager()
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update game state
        game_manager.update(dt)
        
        # Render frame
        game_manager.draw()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
