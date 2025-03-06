from typing import Dict, Optional
from .tetromino import Tetromino
from .board import Board

class GameState:
    """Manages the overall state of the Tetris game."""

    # Scoring system
    SCORING = {
        1: 100,   # Single line
        2: 300,   # Double
        3: 500,   # Triple
        4: 800    # Tetris
    }

    def __init__(self):
        """Initialize a new game state."""
        self.board = Board()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.piece_position = {'x': 0, 'y': 0}
        self.game_paused = False
        self.game_over = False
        
        # Debug flag
        self.debug = True
        
        # Initialize pieces
        self._spawn_new_piece()

    def _spawn_new_piece(self) -> bool:
        """Spawn a new piece at the top of the board."""
        self.current_piece = self.next_piece if self.next_piece else Tetromino.get_random_piece()
        self.next_piece = Tetromino.get_random_piece()
        
        # Calculate starting position (center-top of board)
        self.piece_position = {
            'x': (Board.WIDTH - self.current_piece.get_width()) // 2,
            'y': 0
        }
        
        if self.debug:
            print(f"Spawning new piece at position x:{self.piece_position['x']}, y:{self.piece_position['y']}")
        
        # Check if piece can be placed at starting position
        if not self.board.is_valid_move(self.current_piece, 
                                      self.piece_position['x'], 
                                      self.piece_position['y']):
            self.game_over = True
            if self.debug:
                print("Game Over: Can't place new piece")
            return False
        return True

    def move_piece(self, dx: int, dy: int) -> bool:
        """Try to move the current piece by the given offset."""
        if self.game_over or self.game_paused or not self.current_piece:
            return False

        new_x = self.piece_position['x'] + dx
        new_y = self.piece_position['y'] + dy

        if self.board.is_valid_move(self.current_piece, new_x, new_y):
            self.piece_position['x'] = new_x
            self.piece_position['y'] = new_y
            return True
        return False

    def rotate_piece(self, clockwise: bool = True) -> bool:
        """Try to rotate the current piece."""
        if self.game_over or self.game_paused or not self.current_piece:
            return False

        # Store original shape
        original_shape = self.current_piece.shape
        
        # Rotate piece
        self.current_piece.shape = (self.current_piece.rotate_clockwise() 
                                  if clockwise 
                                  else self.current_piece.rotate_counterclockwise())

        # Try wall kicks
        for dx, dy in self.current_piece.get_wall_kick_tests(self.current_piece.rotation):
            test_x = self.piece_position['x'] + dx
            test_y = self.piece_position['y'] + dy
            
            if self.board.is_valid_move(self.current_piece, test_x, test_y):
                self.piece_position['x'] = test_x
                self.piece_position['y'] = test_y
                return True

        # If no valid rotation found, revert to original shape
        self.current_piece.shape = original_shape
        return False

    def drop_piece(self) -> bool:
        """Move piece down one step. Returns False if piece is locked."""
        if self.move_piece(0, 1):
            return True
        
        if self.debug:
            print("Piece locked, placing on board")
            
        # Lock piece and spawn new one
        self.board.place_piece(self.current_piece, 
                             self.piece_position['x'], 
                             self.piece_position['y'])
        
        # Clear lines and update score
        lines = self.board.clear_lines()
        if lines > 0:
            self.update_score(lines)
        
        return self._spawn_new_piece()

    def hard_drop(self) -> None:
        """Drop piece to the bottom instantly."""
        if self.debug:
            print("Starting hard drop")
            
        # Calculate how far the piece can drop
        cells_dropped = 0
        while self.move_piece(0, 1):
            cells_dropped += 1
            
        if self.debug:
            print(f"Dropped {cells_dropped} cells")
            
        # Add score for the hard drop
        self.score += cells_dropped * 2
        
        # Lock the piece and spawn new one
        self.board.place_piece(self.current_piece, 
                             self.piece_position['x'], 
                             self.piece_position['y'])
        
        # Clear lines and update score
        lines = self.board.clear_lines()
        if lines > 0:
            self.update_score(lines)
            
        # Spawn new piece
        self._spawn_new_piece()

    def update_score(self, lines_cleared: int) -> None:
        """Update score based on lines cleared."""
        if lines_cleared in self.SCORING:
            self.score += self.SCORING[lines_cleared] * self.level
            self.lines_cleared += lines_cleared
            self.level = (self.lines_cleared // 10) + 1

    def get_ghost_position(self) -> Dict[str, int]:
        """Get the position where the piece would land."""
        if not self.current_piece:
            return self.piece_position

        ghost_y = self.board.get_ghost_position(
            self.current_piece,
            self.piece_position['x'],
            self.piece_position['y']
        )
        
        return {
            'x': self.piece_position['x'],
            'y': ghost_y
        }

    def toggle_pause(self) -> None:
        """Toggle the game's pause state."""
        self.game_paused = not self.game_paused

    def get_drop_delay(self) -> int:
        """Calculate delay between piece drops based on level."""
        return max(50, 800 - (self.level * 50))  # in milliseconds