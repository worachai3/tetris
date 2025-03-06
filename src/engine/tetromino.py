from typing import List, Tuple
import random

class Tetromino:
    """Represents a Tetris piece with its shape and rotations."""

    # Tetromino shapes and their rotations
    SHAPES = {
        'I': [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
        ],
        'O': [
            [[1, 1],
             [1, 1]],
        ],
        'T': [
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]],
        ],
        'S': [
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]],
        ],
        'Z': [
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]],
        ],
        'J': [
            [[1, 0, 0],
             [1, 1, 1],
             [0, 0, 0]],
        ],
        'L': [
            [[0, 0, 1],
             [1, 1, 1],
             [0, 0, 0]],
        ],
    }

    # Color codes for each piece (1-7)
    COLORS = {
        'I': 1,  # Cyan
        'O': 2,  # Yellow
        'T': 3,  # Purple
        'S': 4,  # Green
        'Z': 5,  # Red
        'J': 6,  # Blue
        'L': 7,  # Orange
    }

    def __init__(self, shape_name: str = None):
        """Initialize a new tetromino with a random shape if none specified."""
        # Debug flag
        self.debug = True
        
        if shape_name is None:
            shape_name = random.choice(list(self.SHAPES.keys()))
        
        self.shape_name = shape_name
        self.shape = self.SHAPES[shape_name][0]
        self.color = self.COLORS[shape_name]
        self.rotation = 0
        
        if self.debug:
            print(f"\nCreating new Tetromino:")
            print(f"Shape name: {self.shape_name}")
            print(f"Color: {self.color}")
            print("Shape:")
            for row in self.shape:
                print(row)

    def rotate_clockwise(self) -> List[List[int]]:
        """Return the clockwise rotation of the current shape."""
        N = len(self.shape)
        return [[self.shape[N - 1 - j][i] for j in range(N)]
                for i in range(N)]

    def rotate_counterclockwise(self) -> List[List[int]]:
        """Return the counterclockwise rotation of the current shape."""
        N = len(self.shape)
        return [[self.shape[j][N - 1 - i] for j in range(N)]
                for i in range(N)]

    def get_wall_kick_tests(self, rotation: int) -> List[Tuple[int, int]]:
        """Return wall kick test coordinates for rotation."""
        # Simple wall kick tests - can be expanded to implement SRS
        if self.shape_name == 'I':
            return [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)]
        else:
            return [(0, 0), (-1, 0), (1, 0), (0, -1)]

    @classmethod
    def get_random_piece(cls) -> 'Tetromino':
        """Create a new random tetromino."""
        piece = cls()
        if piece.debug:
            print("\nCreated random piece:")
            print(f"Shape name: {piece.shape_name}")
            print(f"Color: {piece.color}")
        return piece

    def get_width(self) -> int:
        """Return the width of the current piece."""
        return len(self.shape[0])

    def get_height(self) -> int:
        """Return the height of the current piece."""
        return len(self.shape)

    def __str__(self) -> str:
        """Return string representation of the piece."""
        return f"Tetromino({self.shape_name})"