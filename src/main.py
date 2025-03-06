import pygame
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engine.game_state import GameState
from src.ui.renderer import Renderer
from src.ui.input_handler import InputHandler

class TetrisGame:
    """Main game class that coordinates all game components."""
    
    def __init__(self, window_size=(800, 600)):
        """Initialize the game with its components."""
        self.game_state = GameState()
        self.renderer = Renderer(window_size)
        self.input_handler = InputHandler()
        self.clock = pygame.time.Clock()
        self.last_drop_time = pygame.time.get_ticks()

    def run(self):
        """Main game loop."""
        try:
            while True:
                # Handle input (returns False if game should quit)
                if not self.input_handler.handle_input(self.game_state):
                    break

                # Update game state
                if not self.game_state.game_over and not self.game_state.game_paused:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_drop_time > self.game_state.get_drop_delay():
                        self.game_state.drop_piece()
                        self.last_drop_time = current_time

                    # Handle held keys for continuous movement
                    held_keys = self.input_handler.get_held_keys()
                    if held_keys['down']:
                        self.game_state.score += 1  # Bonus point for soft drop

                # Render current frame
                self.renderer.render(self.game_state)

                # Maintain frame rate
                self.clock.tick(60)

        except Exception as e:
            print(f"Error occurred: {e}")
            raise
        finally:
            self.quit()

    def quit(self):
        """Clean up and quit the game."""
        pygame.quit()
        sys.exit()

def main():
    """Entry point of the game."""
    try:
        # Initialize pygame
        pygame.init()
        
        # Create and run game
        game = TetrisGame()
        game.run()
    except Exception as e:
        print(f"Failed to start game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()