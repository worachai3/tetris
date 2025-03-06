import pygame
from typing import Optional, Dict, Any
from pygame.event import Event
from src.engine.game_state import GameState

class InputHandler:
    """Handles keyboard input for the Tetris game."""

    def __init__(self):
        """Initialize input handler with default settings."""
        # Key repeat only for movement keys
        pygame.key.set_repeat(200, 50)
        
        # Track if spacebar is being held
        self.space_pressed = False
        
        # Key bindings
        self.controls = {
            pygame.K_LEFT: 'move_left',
            pygame.K_RIGHT: 'move_right',
            pygame.K_DOWN: 'soft_drop',
            pygame.K_UP: 'rotate_clockwise',
            pygame.K_z: 'rotate_counterclockwise',
            pygame.K_SPACE: 'hard_drop',
            pygame.K_p: 'pause',
            pygame.K_ESCAPE: 'quit'
        }
        
        # Action cooldowns (milliseconds)
        self.cooldowns = {
            'move_left': 100,
            'move_right': 100,
            'soft_drop': 50,
            'rotate_clockwise': 200,
            'rotate_counterclockwise': 200
        }
        
        # Last action timestamps
        self.last_action_time: Dict[str, int] = {}
        
        # Debug flags
        self.debug = True

    def handle_input(self, game_state: GameState) -> bool:
        """
        Handle input events and update game state accordingly.
        Returns False if the game should quit, True otherwise.
        """
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle spacebar press and release separately
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.debug:
                    print("Spacebar released")
                self.space_pressed = False
                continue

            if event.type == pygame.KEYDOWN:
                if self.debug:
                    print(f"Key pressed: {pygame.key.name(event.key)}")
                
                # Special handling for spacebar
                if event.key == pygame.K_SPACE:
                    if not self.space_pressed:  # Only trigger hard drop if spacebar wasn't already pressed
                        if self.debug:
                            print("Hard drop triggered")
                        self.space_pressed = True
                        self._handle_action('hard_drop', game_state)
                    continue

                # Handle other keys normally
                action = self.controls.get(event.key)
                if not action:
                    continue

                # Check cooldown for repeatable actions
                if action in self.cooldowns:
                    last_time = self.last_action_time.get(action, 0)
                    if current_time - last_time < self.cooldowns[action]:
                        if self.debug:
                            print(f"Action {action} blocked by cooldown")
                        continue
                    self.last_action_time[action] = current_time
                    if self.debug:
                        print(f"Action {action} executed")

                # Handle the action
                if self._handle_action(action, game_state) is False:
                    return False

        return True

    def _handle_action(self, action: str, game_state: GameState) -> Optional[bool]:
        """
        Handle a single game action.
        Returns False if the game should quit, None otherwise.
        """
        if game_state.game_over and action != 'quit':
            return None

        if action == 'quit':
            return False
        
        if action == 'pause':
            game_state.toggle_pause()
            return None

        if game_state.game_paused:
            return None

        # Movement actions
        if action == 'move_left':
            game_state.move_piece(-1, 0)
        elif action == 'move_right':
            game_state.move_piece(1, 0)
        elif action == 'soft_drop':
            game_state.move_piece(0, 1)
        
        # Rotation actions
        elif action == 'rotate_clockwise':
            game_state.rotate_piece(clockwise=True)
        elif action == 'rotate_counterclockwise':
            game_state.rotate_piece(clockwise=False)
        
        # Hard drop
        elif action == 'hard_drop':
            if self.debug:
                print("Executing hard drop")
            game_state.hard_drop()

        return None

    def get_held_keys(self) -> Dict[str, bool]:
        """Return dictionary of currently held keys."""
        keys = pygame.key.get_pressed()
        return {
            'left': keys[pygame.K_LEFT],
            'right': keys[pygame.K_RIGHT],
            'down': keys[pygame.K_DOWN]
            # Removed space from held keys check
        }