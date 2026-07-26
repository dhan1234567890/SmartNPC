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
        
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # Update game state
        game_manager.update(dt, mouse_clicked=mouse_clicked)
        
        # Render frame
        game_manager.draw()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
