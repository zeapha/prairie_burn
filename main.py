import pygame
import sys
from game import Game

# Initialize pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prairie Burn")

# Colors
BLACK = (0, 0, 0)

# Clock for controlling game speed
clock = pygame.time.Clock()
FPS = 30

# Create game instance
game = Game(screen)

# Main game loop
def main():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to game
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw everything
        game.draw()
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()