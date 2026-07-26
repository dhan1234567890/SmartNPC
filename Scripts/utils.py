import pygame
import math

def has_line_of_sight(start_pos, end_pos, obstacles):
    """
    Returns True if there is a clear line of sight between start_pos and end_pos.
    Returns False if any obstacle intersects the line.
    """
    for obs in obstacles:
        # pygame.Rect.clipline returns a tuple of the intersection points if the line intersects the rect,
        # otherwise it returns an empty tuple.
        if obs.clipline(start_pos, end_pos):
            return False
    return True

def get_cover_position(npc_rect, player_rect, obstacles):
    """
    Finds the best position behind an obstacle to hide from the player.
    """
    best_cover = None
    best_dist = float('inf')
    
    for obs in obstacles:
        # Calculate a point on the opposite side of the obstacle from the player
        # We find the center of the obstacle, and extend a vector away from the player
        dx = obs.centerx - player_rect.centerx
        dy = obs.centery - player_rect.centery
        length = math.hypot(dx, dy)
        
        if length == 0:
            continue
            
        dir_x = dx / length
        dir_y = dy / length
        
        # Move slightly past the obstacle center to the other side
        # Obstacles are roughly 50-200 wide, so push out by ~max dimension
        cover_x = obs.centerx + dir_x * (obs.width / 2 + 20)
        cover_y = obs.centery + dir_y * (obs.height / 2 + 20)
        cover_pos = (cover_x, cover_y)
        
        # Check distance from NPC to this cover spot
        dist_to_cover = math.hypot(cover_x - npc_rect.centerx, cover_y - npc_rect.centery)
        
        # We want the closest cover that blocks line of sight
        if dist_to_cover < best_dist:
            # Verify that standing at this cover position blocks line of sight to player
            if not has_line_of_sight(cover_pos, player_rect.center, obstacles):
                best_dist = dist_to_cover
                best_cover = cover_pos
                
    return best_cover
