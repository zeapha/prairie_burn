import pygame
from grid import Grid
from player import Player
from level import Level
from fire import Fire

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.level_number = 1
        self.load_level(self.level_number)
        self.time_step = 0
        self.game_over = False
        self.victory = False
        self.font = pygame.font.SysFont(None, 36)
        
        # Game state: 0=setup, 1=playing
        self.state = 0
        
        # Setup phase: how many wet squares can be placed
        self.wet_squares_left = self.grid.get_prairie_count() // 2
        
    def load_level(self, level_number):
        # Load level data
        level_data = Level(level_number)
        self.grid_size = level_data.grid_size
        
        # Create grid
        self.grid = Grid(self.screen, level_data)
        
        # Create player at starting position
        self.player = Player(self.grid, level_data.start_pos)
        
        # Create fire manager
        self.fire = Fire(self.grid)
    
    def handle_event(self, event):
        if self.game_over:
            # Restart game on any key press when game is over
            if event.type == pygame.KEYDOWN:
                self.__init__(self.screen)
            return
            
        if event.type == pygame.KEYDOWN:
            if self.state == 0:  # Setup phase
                if event.key == pygame.K_SPACE and self.wet_squares_left == 0:
                    # Start playing when all wet squares are placed
                    self.state = 1
                    return
                    
                # During setup, arrow keys select cells
                self.player.handle_movement(event)
                
                # Add water during setup with W key
                if event.key == pygame.K_w and self.wet_squares_left > 0:
                    row, col = self.player.get_adjacent_cell()
                    if row is not None and col is not None:
                        if self.grid.add_water(row, col):
                            self.wet_squares_left -= 1
                        
            elif self.state == 1:  # Playing phase
                # Player movement - this happens BEFORE fire spreads
                player_moved = False
                if self.player.handle_movement(event):
                    player_moved = True
                
                # Adding water (W key)
                if event.key == pygame.K_w:
                    row, col = self.player.get_adjacent_cell()
                    if row is not None and col is not None:
                        self.grid.add_water(row, col)
                
                # Starting fire (F key)
                if event.key == pygame.K_f:
                    row, col = self.player.get_adjacent_cell()
                    if row is not None and col is not None:
                        self.fire.start_fire(row, col)
                
                # Only update the time step if the player moved
                if player_moved:
                    self.time_step += 1
                    # Now update fire after player has moved
                    self.update_time_step()
    
    def update_time_step(self):
        # Update grid for this time step
        self.grid.update_time_step()
        
        # Check if fire is touching player AFTER fire has spread
        if self.grid.is_fire_adjacent_to_player(self.player.row, self.player.col):
            # Move player to random adjacent cell
            self.player.move_to_random_safe_cell()
            
        # Check win/loss conditions
        if self.grid.is_all_prairie_burned():
            self.victory = True
            self.game_over = True
        elif self.grid.is_non_prairie_burned():
            self.game_over = True
            
    def update(self):
        pass  # Most updates happen in handle_event or time_step
        
    def draw(self):
        # Draw grid
        self.grid.draw()
        
        # Draw fire effects
        self.fire.draw_flames()
        
        # Draw player
        self.player.draw()
        
        # Draw UI
        if self.state == 0:
            # Setup phase
            text = f"Setup Phase: {self.wet_squares_left} wet squares remaining"
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20))
            text2 = "Arrow keys to move, SHIFT+arrow to turn without moving"
            text_surface2 = self.font.render(text2, True, (255, 255, 255))
            self.screen.blit(text_surface2, (20, 60))
            text3 = "W to add water in the direction you face, SPACE to start"
            text_surface3 = self.font.render(text3, True, (255, 255, 255))
            self.screen.blit(text_surface3, (20, 100))
        else:
            # Playing phase
            text = f"Time Step: {self.time_step}"
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20))
            text2 = "Arrow keys to move (advances time), SHIFT+arrow to turn only"
            text_surface2 = self.font.render(text2, True, (255, 255, 255))
            self.screen.blit(text_surface2, (20, 60))
            text3 = "W=water, F=fire in the direction you face"
            text_surface3 = self.font.render(text3, True, (255, 255, 255))
            self.screen.blit(text_surface3, (20, 100))
            
        # Draw game over message
        if self.game_over:
            if self.victory:
                message = "You Win! Press any key to restart"
            else:
                message = "Game Over! Press any key to restart"
            
            text_surface = self.font.render(message, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(text_surface, text_rect)