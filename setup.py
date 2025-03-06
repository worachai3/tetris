#!/usr/bin/env python3

import os
import sys
import subprocess
import venv

def setup_game():
    """Set up the Tetris game environment."""
    
    print("Setting up Tetris game environment...")
    
    # Create virtual environment
    print("\n1. Creating virtual environment...")
    venv.create("venv", with_pip=True)
    
    # Determine the Python executable path in the virtual environment
    if sys.platform == "win32":
        python_path = os.path.join("venv", "Scripts", "python.exe")
        pip_path = os.path.join("venv", "Scripts", "pip.exe")
    else:
        python_path = os.path.join("venv", "bin", "python")
        pip_path = os.path.join("venv", "bin", "pip")
    
    # Install requirements
    print("\n2. Installing requirements...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    print("\n3. Setup complete!")
    print("\nTo run the game:")
    print("1. Activate the virtual environment:")
    if sys.platform == "win32":
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the game:")
    print("   python src/main.py")

if __name__ == "__main__":
    setup_game()