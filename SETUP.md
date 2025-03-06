# Running the Tetris Game

## Prerequisites

### On macOS:
1. Install Homebrew (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install SDL2 dependencies:
```bash
brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf
```

### On Linux (Ubuntu/Debian):
```bash
sudo apt-get install python3-pygame
```

### On Windows:
No additional prerequisites needed.

## Setup Instructions

1. Make sure you have Python 3.8+ installed:
```bash
python --version
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

4. Run the game:
```bash
# From the tetris directory
python src/main.py
```

## Controls
- ←/→: Move piece left/right
- ↑: Rotate piece clockwise
- Z: Rotate piece counter-clockwise
- ↓: Soft drop
- Space: Hard drop
- P: Pause game
- ESC: Quit game

## Troubleshooting

If you encounter pygame installation issues:

### On macOS:
1. Make sure SDL2 is installed:
```bash
brew list sdl2
```
If not listed, install it:
```bash
brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf
```

2. Try installing pygame with additional flags:
```bash
pip install --upgrade pip
pip install pygame --pre
```

### On Linux:
Try installing system pygame package:
```bash
sudo apt-get update
sudo apt-get install python3-pygame
```

### On Windows:
Try installing pygame with:
```bash
pip install pygame --pre
```

If problems persist:
1. Check Python version compatibility
2. Try creating a new virtual environment
3. Check for system-specific installation guides at: https://www.pygame.org/wiki/GettingStarted