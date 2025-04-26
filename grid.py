import pygame
import random

# Cell types
EMPTY = 0
PRAIRIE = 1
OTHER_PLANTS = 2

# Cell states
DRY = 0
WET = 1
BURNING = 2
BURNED = 3

class Grid:
    def __init__(self, screen, level_data):
        self.screen = screen
        self.rows = level_data.grid_size
        self.cols = level_data.grid_size
        self.grid_data = level_data.grid_data
        
        # Calculate cell size based on screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.cell_size = min((screen_width - 100) // self.cols, 
                             (screen_height - 200) // self.rows)
        
        # Initialize grid position to center it
        self.grid_x = (screen_width - (self.cols * self.cell_size)) // 2
        self.grid_y = (screen_height - (self.rows * self.cell_size)) // 2 + 50
        
        # Initialize cell states (all dry initially)
        self.cell_states = [[DRY for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Track wet cells and their time steps
        self.wet_cells = {}  # (row, col): time_step
        
        # Track burning cells for fire spread
        self.burning_cells = []

    def get_prairie_count(self):
        """Count the number of prairie cells"""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid_data[row][col] == PRAIRIE:
                    count += 1
        return count
    
    def is_valid_cell(self, row, col):
        """Check if coordinates are within grid"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def add_water(self, row, col):
        """Add water to a cell"""
        if not self.is_valid_cell(row, col):
            return False
            
        # Can't wet cells that are burning or burned
        if self.cell_states[row][col] in [BURNING, BURNED]:
            return False
            
        # Set cell to wet state
        self.cell_states[row][col] = WET
        self.wet_cells[(row, col)] = 0  # Start counting time steps
        return True
    
    def add_fire(self, row, col):
        """Start a fire in a cell"""
        if not self.is_valid_cell(row, col):
            return False
            
        # Can only burn prairie that is dry
        if (self.grid_data[row][col] == PRAIRIE and 
            self.cell_states[row][col] == DRY):
            self.cell_states[row][col] = BURNING
            self.burning_cells.append((row, col))
            return True
        return False
    
    # In grid.py, update this method:
    def is_cell_walkable(self, row, col):
        """Check if player can walk on this cell"""
        if not self.is_valid_cell(row, col):
            return False
        # Player can't walk on burning cells
        return self.cell_states[row][col] != BURNING

    
    def get_adjacent_cells(self, row, col):
        """Get all valid adjacent cells"""
        adjacent = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_cell(new_row, new_col):
                adjacent.append((new_row, new_col))
        return adjacent
    
    def is_fire_adjacent_to_player(self, player_row, player_col):
        """Check if fire is adjacent to player"""
        adjacent_cells = self.get_adjacent_cells(player_row, player_col)
        for row, col in adjacent_cells:
            if self.cell_states[row][col] == BURNING:
                return True
        return False
    
    def update_time_step(self):
        """Update grid for a time step"""
        # Update wet cells (dry after 10 steps)
        cells_to_dry = []
        for (row, col), steps in self.wet_cells.items():
            self.wet_cells[(row, col)] = steps + 1
            if steps + 1 >= 10:
                cells_to_dry.append((row, col))
                
        for row, col in cells_to_dry:
            del self.wet_cells[(row, col)]
            if self.cell_states[row][col] == WET:  # Only change if still wet
                self.cell_states[row][col] = DRY
        
        # Spread fire
        new_burning_cells = []
        for row, col in self.burning_cells:
            # Each burning cell burns for exactly one turn
            self.cell_states[row][col] = BURNED
            
            # Try to spread fire to adjacent cells
            adjacent_cells = self.get_adjacent_cells(row, col)
            random.shuffle(adjacent_cells)  # Randomize spread direction
            
            # Keep trying until fire spreads to at least one cell
            # or until we've tried all possible directions
            spread_success = False
            for new_row, new_col in adjacent_cells:
                # Fire can spread to any dry cell (prairie or other plants)
                if self.cell_states[new_row][new_col] == DRY:
                    self.cell_states[new_row][new_col] = BURNING
                    new_burning_cells.append((new_row, new_col))
                    spread_success = True
                    break  # Successfully spread to one cell
                    
            # If fire couldn't spread anywhere (surrounded by wet or burned cells),
            # it just goes out
                
        # Update burning cells list
        self.burning_cells = new_burning_cells

    def is_all_prairie_burned(self):
        """Check if all prairie cells are burned"""
        for row in range(self.rows):
            for col in range(self.cols):
                if (self.grid_data[row][col] == PRAIRIE and 
                    self.cell_states[row][col] not in [BURNED, BURNING]):
                    return False
        return True
    
    def is_non_prairie_burned(self):
        """Check if any non-prairie cell is burned"""
        for row in range(self.rows):
            for col in range(self.cols):
                if (self.grid_data[row][col] == OTHER_PLANTS and 
                    self.cell_states[row][col] in [BURNED, BURNING]):
                    return True
        return False
    
    def draw(self):
        """Draw the grid"""
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate cell position
                x = self.grid_x + col * self.cell_size
                y = self.grid_y + row * self.cell_size
                
                # Get cell type and state
                cell_type = self.grid_data[row][col]
                cell_state = self.cell_states[row][col]
                
                # Set color based on cell type and state
                if cell_type == EMPTY:
                    color = (100, 100, 100)  # Gray for empty
                elif cell_type == PRAIRIE:
                    if cell_state == DRY:
                        color = (210, 180, 140)  # Yellowish brown for prairie
                    elif cell_state == WET:
                        color = (150, 130, 100)  # Darker brown for wet prairie
                    elif cell_state == BURNING:
                        color = (255, 0, 0)      # Red for burning
                    else:  # BURNED
                        color = (50, 50, 50)     # Dark gray for burned
                else:  # OTHER_PLANTS
                    if cell_state == DRY:
                        color = (0, 150, 0)      # Green for plants
                    elif cell_state == WET:
                        color = (0, 100, 0)      # Dark green for wet plants
                    elif cell_state == BURNING:
                        color = (255, 0, 0)      # Red for burning
                    else:  # BURNED
                        color = (50, 50, 50)     # Dark gray for burned
                
                # Draw the cell
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                
                # Draw cell border
                pygame.draw.rect(self.screen, (0, 0, 0), 
                                (x, y, self.cell_size, self.cell_size), 1)
    
    def screen_to_grid(self, screen_x, screen_y):
        """Convert screen coordinates to grid coordinates"""
        # Check if within grid bounds
        if (screen_x < self.grid_x or 
            screen_y < self.grid_y or
            screen_x >= self.grid_x + self.cols * self.cell_size or
            screen_y >= self.grid_y + self.rows * self.cell_size):
            return None, None
            
        # Calculate grid coordinates
        col = (screen_x - self.grid_x) // self.cell_size
        row = (screen_y - self.grid_y) // self.cell_size
        
        return row, col