# Python Tetris Implementation

A modern implementation of the classic Tetris game using Python. This project features a clean architecture with separation of game engine and UI components, making it both maintainable and extensible.

## Project Structure

```
tetris/
├── src/
│   ├── engine/
│   │   ├── board.py       # Game board logic
│   │   ├── game_state.py  # Game state management
│   │   └── tetromino.py   # Tetromino pieces
│   ├── ui/
│   │   ├── input_handler.py  # Input management
│   │   └── renderer.py       # Game rendering
│   └── main.py            # Game entry point
├── tests/
│   └── test_tetromino.py  # Unit tests
└── docs/
    └── architecture.md    # Architecture documentation
```

## Features

- Classic Tetris gameplay mechanics
- Modern code architecture
- Clean separation of concerns
- Unit test coverage
- Configurable game parameters
- Input handling system
- Rendering engine

## Technical Architecture

The project is divided into two main components:

### Game Engine
- Board management
- Tetromino manipulation
- Game state handling
- Collision detection
- Score tracking

### User Interface
- Input handling
- Game rendering
- Visual effects
- User feedback

## Requirements

```
# Core dependencies
pygame
pytest
```

## Installation

1. Set up the development environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the game package:
```bash
pip install -e .
```

## Running the Game

Launch the game:
```bash
python src/main.py
```

## Running Tests

Execute the test suite:
```bash
pytest tests/
```

## Controls

- **Left/Right Arrow**: Move piece
- **Up Arrow**: Rotate piece
- **Down Arrow**: Soft drop
- **Space**: Hard drop
- **P**: Pause game
- **ESC**: Quit game

## Development

The project follows these design principles:
- Separation of concerns
- Single responsibility principle
- Dependency injection
- Test-driven development

## AI Disclaimer

This project was created with the assistance of artificial intelligence (Roo AI). While the implementation and architecture were developed through AI collaboration, the project demonstrates software engineering best practices and game development patterns.

## License

This project is open-source and available for educational purposes. Tetris® is a registered trademark of The Tetris Company, LLC.