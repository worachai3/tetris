class Board:
    """Represents the Tetris game board."""
    
    WIDTH = 10
    HEIGHT = 20
    EMPTY_CELL = 0

    def __init__(self):
        """Initialize an empty board."""
        self.grid = [[self.EMPTY_CELL for _ in range(self.WIDTH)] 
                    for _ in range(self.HEIGHT)]
        self.current_piece = None
        self.game_over = False

    def is_valid_move(self, piece, offset_x, offset_y):
        """Check if the piece can move to the specified position."""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = x + offset_x
                    new_y = y + offset_y
                    if (new_x < 0 or new_x >= self.WIDTH or
                        new_y >= self.HEIGHT or
                        (new_y >= 0 and self.grid[new_y][new_x] != self.EMPTY_CELL)):
                        return False
        return True

    def place_piece(self, piece, pos_x, pos_y):
        """Place a piece on the board at the specified position."""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell and 0 <= y + pos_y < self.HEIGHT:
                    self.grid[y + pos_y][x + pos_x] = piece.color

    def clear_lines(self):
        """Clear completed lines and return the number of lines cleared."""
        lines_cleared = 0
        y = self.HEIGHT - 1
        while y >= 0:
            if all(cell != self.EMPTY_CELL for cell in self.grid[y]):
                lines_cleared += 1
                # Move all lines above down
                for move_y in range(y, 0, -1):
                    self.grid[move_y] = self.grid[move_y - 1][:]
                self.grid[0] = [self.EMPTY_CELL] * self.WIDTH
            else:
                y -= 1
        return lines_cleared

    def get_ghost_position(self, piece, pos_x, pos_y):
        """Calculate the landing position of the current piece."""
        ghost_y = pos_y
        while self.is_valid_move(piece, pos_x, ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def is_game_over(self):
        """Check if any column in the top row is filled."""
        return any(cell != self.EMPTY_CELL for cell in self.grid[0])

    def get_grid_copy(self):
        """Return a copy of the current grid."""
        return [row[:] for row in self.grid]