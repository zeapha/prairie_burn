# Prairie Burn Game

A fun game where you control a prairie burn! Help maintain the ecosystem by carefully burning the prairie while protecting other plants.

## How to Play

1. **Start the game** by running `python main.py` in your terminal
2. **Setup Phase**:
   - Use arrow keys to move around
   - Hold SHIFT + arrow keys to turn without moving
   - Press W to wet squares in the direction you're facing (you get a number of wet squares equal to half the prairie size)
   - Press SPACE when you're ready to start the burn

3. **Playing Phase**:
   - Use arrow keys to move around (each step advances time)
   - Hold SHIFT + arrow keys to turn without advancing time
   - Press W to wet adjacent squares in the direction you're facing
   - Press F to start a fire in the square you're facing

4. **Goal**: Burn all the prairie (yellowish-brown) without letting the fire spread to other plants (green)

5. **Rules**:
   - Fire spreads randomly to adjacent prairie squares each turn
   - Wet squares stay wet for 10 turns
   - You can't move into fire
   - If fire is next to you, you'll move to a random safe square

## Levels

The game has multiple levels of increasing difficulty:
- Level 1: Small square prairie (easy)
- Level 2: Medium-sized prairie with a circular shape
- Level 3: Large prairie with a complex shape
- Higher levels: Randomly generated prairie shapes that get bigger and more complex!

Have fun playing and learning about controlled prairie burns!