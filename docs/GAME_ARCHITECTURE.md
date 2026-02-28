# Game Architecture

## 1. Main Components

### 1.1 Rendering and Assets
- `pygame` window (`800x600`)
- background generated in code (pink vignette gradient)
- snake sprite (`pink_cat.png`)
- food sprite (`mouse_pink.png`)
- custom fonts for score, menu, end/win text

### 1.2 UI States
- **Start Menu**
  - start button
  - last highscore message
  - special birthday text when last highscore is `20`
- **Playing**
  - snake movement, food collection, score updates
- **Lose Screen**
  - collision result
  - continue (`C`) / quit (`Q`)
- **Win Screen**
  - triggered at score `20`
  - confetti animation
  - birthday text
  - continue (`C`) / quit (`Q`)

### 1.3 Game Data
- snake body list (grid cells)
- current direction + next requested direction
- current food position
- score (`length_of_snake - 1`)
- last highscore (stored during runtime session)

## 2. Core Mechanisms

### 2.1 Movement Model
- **Logic**: discrete grid movement by one full cell (`cat_size`) per tick.
- **Render**: interpolated positions between logic ticks for visual smoothness.

Why this matters:
- grid logic gives predictable collision and clean body alignment
- interpolation keeps movement from looking jumpy

### 2.2 Collision Handling
- wall collision: head outside screen bounds -> lose state
- self collision: head equals any body cell -> lose state
- food collision: head rectangle overlaps food rectangle -> grow + respawn food

### 2.3 Direction Safety
- instant 180-degree reversal is blocked
- prevents immediate self-collisions from opposite-direction input in one step

### 2.4 Food Spawn Rules
Food is chosen from valid candidate cells:
- not on edges/corners (1-cell margin)
- not inside snake body

This removes unfair placements that force risky or instant-loss moves.

### 2.5 Win Condition
- when score reaches `20`, gameplay halts and transitions to win screen
- win screen displays:
  - `Happy 20th Birthday Mia Maus`
  - animated pink confetti

## 3. State Flow

1. App starts in Start Menu.
2. Player starts round.
3. Round ends in either:
   - Lose state (wall/body hit), or
   - Win state (score 20).
4. Player can restart (`C`) or quit (`Q`).
5. Menu reflects latest highscore for next round.

## 4. Main Challenges and Solutions

### Challenge A: Early false self-collisions after growth
Root cause:
- large sprite size with pixel-based movement/history spacing introduced overlap artifacts.

Fix:
- moved to strict grid logic for body positions and collisions.

### Challenge B: Movement felt too fast/jumpy after grid fix
Root cause:
- one-step-per-cell can appear abrupt at low frame rates.

Fix:
- separated logic tick from render tick and added interpolation.

### Challenge C: Food spawned in impractical border locations
Root cause:
- random spawn across entire field included extreme edge cells.

Fix:
- constrained spawn area and excluded occupied snake cells.

### Challenge D: Recursive loop restarts
Root cause:
- calling game loop from inside lose/win handlers can grow call stack.

Fix:
- switched to a top-level menu/round flow that returns cleanly between states.

## 5. Extension Ideas
- Persist highscore to disk (JSON file) instead of session-only memory.
- Add mobile-friendly touch controls (for future web/mobile port).
- Add difficulty scaling (speed increase by score).
- Add sound effects and celebration music for win state.
