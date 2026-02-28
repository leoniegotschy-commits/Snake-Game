# Snake-Game
Birthday-themed Snake game with a pink visual style, custom sprites, and a special celebration screen at score 20.

## Project Purpose
This game is a personal birthday surprise with classic Snake gameplay and custom presentation:
- pink cat sprite as the snake body
- pink mouse sprite as food
- soft pink vignette background
- win condition at score `20` with confetti and birthday message

## Current Feature Set
- Start menu with:
  - `Start Game` button
  - last highscore display
  - `Happy Birthday` text when last highscore is exactly `20`
- Manual snake controls with arrow keys
- Smooth visual movement (interpolation) on top of grid-accurate logic
- Safe food spawning:
  - avoids border/corner cells
  - avoids snake body cells
- Lose state (wall/self-collision)
- Win state at score `20`:
  - text: `Happy 20th Birthday Mia Maus`
  - animated pink confetti

## Quick Run
1. Install dependencies:
   - `pip install pygame`
2. Run:
   - `python game.py`

## Controls
- In menu:
  - Mouse click `Start Game` or press `Enter`/`Space`
  - `Q` to quit
- In game:
  - Arrow keys to move
- In lose/win screens:
  - `C` to return/start a new round
  - `Q` to quit

## Technical Notes
- Gameplay logic is grid-based (one cell per move), which keeps collision behavior stable.
- Rendering is frame-based with interpolation between grid steps for smoother motion.
- This separation was important to fix earlier issues where large sprites and pixel-step movement caused false/instant collisions.

## Documentation
Detailed technical breakdown is in:
- [Game Architecture](./docs/GAME_ARCHITECTURE.md)
