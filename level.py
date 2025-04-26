import random

# Cell types
EMPTY = 0
PRAIRIE = 1
OTHER_PLANTS = 2

class Level:
    def __init__(self, level_number):
        # Initialize level based on level number
        if level_number == 1:
            self.create_level_1()
        elif level_number == 2:
            self.create_level_2()
        elif level_number == 3:
            self.create_level_3()
        else:
            # Create random level for higher numbers
            self.create_random_level(level_number)
    
    def create_level_1(self):
        """Small simple square level"""
        self.grid_size = 7
        self.grid_data = [[OTHER_PLANTS for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Create a small prairie area in the center
        for row in range(2, 5):
            for col in range(2, 5):
                self.grid_data[row][col] = PRAIRIE
                
        # Player starts in the corner of the prairie
        self.start_pos = (2, 2)
    
    def create_level_2(self):
        """Medium sized level with more complex shape"""
        self.grid_size = 10
        self.grid_data = [[OTHER_PLANTS for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Create a bigger prairie area in the center with a more complex shape
        prairie_pattern = [
            "  PPP  ",
            " PPPPP ",
            "PPPPPPP",
            "PPPPPPP",
            "PPPPPPP",
            " PPPPP ",
            "  PPP  "
        ]
        
        # Center the pattern
        start_row = (self.grid_size - len(prairie_pattern)) // 2
        start_col = (self.grid_size - len(prairie_pattern[0])) // 2
        
        # Apply the pattern
        for r, row in enumerate(prairie_pattern):
            for c, cell in enumerate(row):
                if cell == 'P':
                    self.grid_data[start_row + r][start_col + c] = PRAIRIE
        
        # Player starts in the corner of the prairie
        self.start_pos = (start_row, start_col + 3)  # Adjusted to be in the prairie
    
    def create_level_3(self):
        """Larger level with even more complex shape"""
        self.grid_size = 15
        self.grid_data = [[OTHER_PLANTS for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Create a more complex prairie shape
        prairie_pattern = [
            "    PPPPP    ",
            "   PPPPPPP   ",
            "  PPPPPPPPP  ",
            " PPPPPPPPPPP ",
            "PPPPPPPPPPPPP",
            "PPPPP   PPPPP",
            "PPPP     PPPP",
            "PPPPP   PPPPP",
            "PPPPPPPPPPPPP",
            " PPPPPPPPPPP ",
            "  PPPPPPPPP  ",
            "   PPPPPPP   ",
            "    PPPPP    "
        ]
        
        # Center the pattern
        start_row = (self.grid_size - len(prairie_pattern)) // 2
        start_col = (self.grid_size - len(prairie_pattern[0])) // 2
        
        # Apply the pattern
        for r, row in enumerate(prairie_pattern):
            for c, cell in enumerate(row):
                if c < len(row) and cell == 'P':  # Check if index is within bounds
                    grid_row = start_row + r
                    grid_col = start_col + c
                    if 0 <= grid_row < self.grid_size and 0 <= grid_col < self.grid_size:
                        self.grid_data[grid_row][grid_col] = PRAIRIE
        
        # Player starts in the left part of the prairie
        self.start_pos = (self.grid_size // 2, start_col + 2)
    
    def create_random_level(self, level_number):
        """Create a random level with increasing difficulty"""
        self.grid_size = 10 + level_number  # Increase size with level
        
        # Create grid with all other plants
        self.grid_data = [[OTHER_PLANTS for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Calculate prairie size (increases with level)
        prairie_size = 5 + level_number // 2
        
        # Create random prairie shape using cellular automata
        # Start with random cells
        center = self.grid_size // 2
        radius = prairie_size // 2
        
        # Create initial random prairie area
        for row in range(center - radius, center + radius + 1):
            for col in range(center - radius, center + radius + 1):
                if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                    # More likely to be prairie near center
                    distance = abs(row - center) + abs(col - center)
                    chance = 0.9 - (distance / (2 * radius)) * 0.6
                    if random.random() < chance:
                        self.grid_data[row][col] = PRAIRIE
        
        # Smooth the shape with cellular automata
        for _ in range(3):
            new_grid = [row[:] for row in self.grid_data]
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    # Count prairie neighbors
                    prairie_count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if (0 <= nr < self.grid_size and 
                                0 <= nc < self.grid_size and 
                                self.grid_data[nr][nc] == PRAIRIE):
                                prairie_count += 1
                    
                    # Apply cellular automata rules
                    if self.grid_data[row][col] == PRAIRIE:
                        # Stay prairie if enough neighbors
                        if prairie_count < 3:
                            new_grid[row][col] = OTHER_PLANTS
                    else:
                        # Become prairie if enough neighbors
                        if prairie_count > 4:
                            new_grid[row][col] = PRAIRIE
            
            self.grid_data = new_grid
        
        # Find a good starting position (in the prairie)
        prairie_cells = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid_data[row][col] == PRAIRIE:
                    prairie_cells.append((row, col))
        
        if prairie_cells:
            self.start_pos = random.choice(prairie_cells)
        else:
            # Fallback if something went wrong
            self.start_pos = (center, center)
            self.grid_data[center][center] = PRAIRIE