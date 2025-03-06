import pygame
from typing import Tuple, Optional
from src.engine.game_state import GameState
from src.engine.board import Board
from src.engine.tetromino import Tetromino

class Renderer:
    """Handles all game rendering using Pygame."""

    # Colors (R, G, B)
    COLORS = {
        0: (40, 40, 40),    # Empty cell
        1: (0, 240, 240),   # Cyan (I)
        2: (240, 240, 0),   # Yellow (O)
        3: (160, 0, 240),   # Purple (T)
        4: (0, 240, 0),     # Green (S)
        5: (240, 0, 0),     # Red (Z)
        6: (0, 0, 240),     # Blue (J)
        7: (240, 160, 0),   # Orange (L)
    }
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600)):
        """Initialize the renderer with the given window size."""
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Tetris")
        
        # Calculate cell size based on window height
        self.cell_size = (window_size[1] - 100) // Board.HEIGHT
        
        # Calculate board position to center it
        self.board_offset_x = (window_size[0] - (Board.WIDTH * self.cell_size)) // 2
        self.board_offset_y = (window_size[1] - (Board.HEIGHT * self.cell_size)) // 2
        
        # Load fonts
        self.font_big = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Debug flag
        self.debug = True

    def draw_cell(self, x: int, y: int, color_idx: int, ghost: bool = False) -> None:
        """Draw a single cell with the specified color."""
        color = self.COLORS[color_idx]
        rect = pygame.Rect(
            self.board_offset_x + x * self.cell_size,
            self.board_offset_y + y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        
        if ghost:
            # Draw ghost piece with transparency
            surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            pygame.draw.rect(surface, (*color, 128), surface.get_rect())
            self.screen.blit(surface, rect)
        else:
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def draw_board(self, game_state: GameState) -> None:
        """Draw the game board and current piece."""
        # Draw board background
        board_rect = pygame.Rect(
            self.board_offset_x,
            self.board_offset_y,
            Board.WIDTH * self.cell_size,
            Board.HEIGHT * self.cell_size
        )
        pygame.draw.rect(self.screen, (0, 0, 0), board_rect)
        
        # Draw grid cells
        for y, row in enumerate(game_state.board.grid):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(x, y, cell)
        
        # Draw ghost piece
        if game_state.current_piece:
            ghost_pos = game_state.get_ghost_position()
            self._draw_piece(game_state.current_piece, ghost_pos['x'], ghost_pos['y'], True)
        
        # Draw current piece
        if game_state.current_piece:
            self._draw_piece(
                game_state.current_piece,
                game_state.piece_position['x'],
                game_state.piece_position['y']
            )

    def _draw_piece(self, piece: Tetromino, x: int, y: int, ghost: bool = False) -> None:
        """Draw a tetromino piece at the specified position."""
        if self.debug:
            print(f"Drawing piece at ({x}, {y})")
            print(f"Piece color: {piece.color}")
            print(f"Piece shape:\n{piece.shape}")
            
        for row_idx, row in enumerate(piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    self.draw_cell(x + col_idx, y + row_idx, piece.color, ghost)

    def draw_next_piece(self, next_piece: Tetromino) -> None:
        """Draw the next piece preview."""
        if self.debug:
            print("\nDrawing next piece preview:")
            print(f"Next piece: {next_piece}")
            if next_piece:
                print(f"Next piece color: {next_piece.color}")
                print(f"Next piece shape:\n{next_piece.shape}")
        
        preview_x = self.board_offset_x + (Board.WIDTH * self.cell_size) + 50
        preview_y = self.board_offset_y + 50
        
        # Draw preview box background
        preview_rect = pygame.Rect(
            preview_x - 10,
            preview_y - 10,
            5 * self.cell_size,
            5 * self.cell_size
        )
        pygame.draw.rect(self.screen, (40, 40, 40), preview_rect)
        
        if not next_piece:
            if self.debug:
                print("No next piece to draw!")
            return
            
        # Draw next piece centered in preview box
        piece_width = len(next_piece.shape[0])
        piece_height = len(next_piece.shape)
        
        x_offset = (4 - piece_width) // 2
        y_offset = (4 - piece_height) // 2
        
        preview_grid_x = preview_x // self.cell_size
        preview_grid_y = preview_y // self.cell_size
        
        if self.debug:
            print(f"Preview box position: ({preview_x}, {preview_y})")
            print(f"Piece dimensions: {piece_width}x{piece_height}")
            print(f"Offset: ({x_offset}, {y_offset})")
            print(f"Final grid position: ({preview_grid_x + x_offset}, {preview_grid_y + y_offset})")
        
        self._draw_piece(
            next_piece,
            preview_grid_x + x_offset,
            preview_grid_y + y_offset
        )

    def draw_score(self, game_state: GameState) -> None:
        """Draw score, level, and lines information."""
        score_x = self.board_offset_x - 200
        score_y = self.board_offset_y + 50
        
        # Draw score
        score_text = self.font_small.render(f"Score: {game_state.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (score_x, score_y))
        
        # Draw level
        level_text = self.font_small.render(f"Level: {game_state.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (score_x, score_y + 40))
        
        # Draw lines cleared
        lines_text = self.font_small.render(f"Lines: {game_state.lines_cleared}", True, (255, 255, 255))
        self.screen.blit(lines_text, (score_x, score_y + 80))

    def draw_game_over(self) -> None:
        """Draw game over screen."""
        overlay = pygame.Surface(self.window_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_big.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2))
        self.screen.blit(text, text_rect)

    def draw_pause(self) -> None:
        """Draw pause screen overlay."""
        overlay = pygame.Surface(self.window_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font_big.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2))
        self.screen.blit(text, text_rect)

    def render(self, game_state: GameState) -> None:
        """Render the complete game frame."""
        self.screen.fill((20, 20, 20))
        self.draw_board(game_state)
        self.draw_next_piece(game_state.next_piece)
        self.draw_score(game_state)
        
        if game_state.game_over:
            self.draw_game_over()
        elif game_state.game_paused:
            self.draw_pause()
            
        pygame.display.flip()