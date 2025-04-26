import pygame
import random

# Cell states (same as in grid.py)
DRY = 0
WET = 1
BURNING = 2
BURNED = 3

class Fire:
    def __init__(self, grid):
        self.grid = grid
        self.burn_time = 1  # How many time steps a cell burns before becoming burned
        
        # Visual effects
        self.flame_colors = [
            (255, 0, 0),      # Red
            (255, 69, 0),     # Orange-Red
            (255, 140, 0),    # Dark Orange
            (255, 165, 0)     # Orange
        ]
        self.flame_particles = []  # For optional particle effects
        
    def start_fire(self, row, col):
        """Start a fire at the given location if possible"""
        return self.grid.add_fire(row, col)
        
    def get_burning_cells(self):
        """Get all currently burning cells"""
        return self.grid.burning_cells
        
    def draw_flames(self):
        """Draw flame effects on burning cells"""
        for row, col in self.grid.burning_cells:
            # Calculate cell position
            x = self.grid.grid_x + col * self.grid.cell_size
            y = self.grid.grid_y + row * self.grid.cell_size
            
            # Draw multiple flame rectangles with different colors
            for i in range(3):
                flame_color = random.choice(self.flame_colors)
                # Random smaller flame inside the cell
                flame_size = int(self.grid.cell_size * 0.4)
                flame_x = x + random.randint(0, self.grid.cell_size - flame_size)
                flame_y = y + random.randint(0, self.grid.cell_size - flame_size)
                
                pygame.draw.rect(self.grid.screen, flame_color, 
                                (flame_x, flame_y, flame_size, flame_size))
    
    def is_fire_out(self):
        """Check if all fires are out"""
        return len(self.grid.burning_cells) == 0