import pygame
import random

class Player:
    def __init__(self, grid, start_pos=None):
        self.grid = grid
        
        # Default starting position (center of grid)
        if start_pos is None:
            self.row = grid.rows // 2
            self.col = grid.cols // 2
        else:
            self.row, self.col = start_pos
            
        # Player color
        self.color = (0, 0, 255)  # Blue
        
        # Size is slightly smaller than grid cell
        self.size = int(grid.cell_size * 0.8)
        
        # Direction: 0=up, 1=right, 2=down, 3=left
        self.direction = 1
        self.direction_indicators = [
            (0, -0.3),  # Up
            (0.3, 0),   # Right
            (0, 0.3),   # Down
            (-0.3, 0)   # Left
        ]
        
    def draw(self):
        """Draw the player on the grid"""
        # Calculate player position (centered in cell)
        x = self.grid.grid_x + self.col * self.grid.cell_size + (self.grid.cell_size - self.size) // 2
        y = self.grid.grid_y + self.row * self.grid.cell_size + (self.grid.cell_size - self.size) // 2
        
        # Draw player
        pygame.draw.rect(self.grid.screen, self.color, (x, y, self.size, self.size))
        
        # Draw direction indicator
        indicator_color = (255, 255, 0)  # Yellow
        dx, dy = self.direction_indicators[self.direction]
        
        # Calculate indicator position
        indicator_size = int(self.size * 0.4)
        indicator_x = x + self.size//2 + int(dx * self.size) - indicator_size//2
        indicator_y = y + self.size//2 + int(dy * self.size) - indicator_size//2
        
        # Draw indicator
        pygame.draw.circle(self.grid.screen, indicator_color, 
                          (indicator_x + indicator_size//2, indicator_y + indicator_size//2), 
                          indicator_size//2)
        
    def handle_movement(self, event):
        """Handle player movement and turning with arrow keys"""
        # Check for turn-only mode (holding SHIFT key)
        turn_only = pygame.key.get_mods() & pygame.KMOD_SHIFT
        
        new_row, new_col = self.row, self.col
        old_direction = self.direction
        
        if event.key == pygame.K_UP:
            self.direction = 0
            if not turn_only:
                new_row -= 1
        elif event.key == pygame.K_RIGHT:
            self.direction = 1
            if not turn_only:
                new_col += 1
        elif event.key == pygame.K_DOWN:
            self.direction = 2
            if not turn_only:
                new_row += 1
        elif event.key == pygame.K_LEFT:
            self.direction = 3
            if not turn_only:
                new_col -= 1
        else:
            return False  # No movement or turning
            
        # If only turning, return False for time step (no time advancement)
        if turn_only:
            return False
            
        # Check if direction changed without moving
        if self.direction != old_direction and new_row == self.row and new_col == self.col:
            return False
            
        # Check if new position is valid
        if self.grid.is_valid_cell(new_row, new_col) and self.grid.is_cell_walkable(new_row, new_col):
            self.row, self.col = new_row, new_col
            return True  # Successful movement (time step advances)
            
        return False  # Movement failed
    
    def get_adjacent_cell(self, event=None):
        """Get cell coordinates adjacent to player based on facing direction"""
        row, col = self.row, self.col
        
        # If event is provided, update direction based on arrow key
        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = 0
            elif event.key == pygame.K_RIGHT:
                self.direction = 1
            elif event.key == pygame.K_DOWN:
                self.direction = 2
            elif event.key == pygame.K_LEFT:
                self.direction = 3
        
        # Use current direction to determine adjacent cell
        if self.direction == 0:  # Up
            row -= 1
        elif self.direction == 1:  # Right
            col += 1
        elif self.direction == 2:  # Down
            row += 1
        elif self.direction == 3:  # Left
            col -= 1
            
        if self.grid.is_valid_cell(row, col):
            return row, col
        return None, None
    
    def move_to_random_safe_cell(self):
        """Move player to a random adjacent cell that is safe"""
        adjacent_cells = []
        
        # Find all safe adjacent cells
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = self.row + dr, self.col + dc
            if (self.grid.is_valid_cell(new_row, new_col) and 
                self.grid.is_cell_walkable(new_row, new_col)):
                adjacent_cells.append((new_row, new_col))
                
        # If there are safe cells, move to one
        if adjacent_cells:
            self.row, self.col = random.choice(adjacent_cells)
        # If no safe cells (completely surrounded by fire),
        # player stays in place and will lose next turn