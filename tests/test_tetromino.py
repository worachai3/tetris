import unittest
from ..src.engine.tetromino import Tetromino

class TestTetromino(unittest.TestCase):
    def test_tetromino_creation(self):
        """Test that tetromino pieces are created correctly."""
        # Test specific piece creation
        t_piece = Tetromino('T')
        self.assertEqual(t_piece.shape_name, 'T')
        self.assertTrue(isinstance(t_piece.color, int))
        
        # Test random piece creation
        random_piece = Tetromino()
        self.assertIn(random_piece.shape_name, Tetromino.SHAPES.keys())

    def test_rotation(self):
        """Test piece rotation functionality."""
        piece = Tetromino('T')
        original_shape = [row[:] for row in piece.shape]
        
        # Test clockwise rotation
        rotated = piece.rotate_clockwise()
        self.assertNotEqual(rotated, original_shape)
        
        # Test four rotations return to original position
        for _ in range(4):
            piece.shape = piece.rotate_clockwise()
        self.assertEqual(piece.shape, original_shape)

if __name__ == '__main__':
    unittest.main()