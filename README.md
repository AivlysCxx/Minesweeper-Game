# MineSweeper

## Project Introduction:
- Our project implements the classic game of Minesweeper in Python. The goal is to uncover all cells without mines.

## Gameplay:
- The player starts by uncovering a cell. 
- If the cell contains a mine, the game ends.
- If the cell does not contain a mine, it displays a number indicating how many adjacent cells contain mines.
- The player uses this information to deduce which neighboring cells are safe to uncover.
- The player can also place flags on cells they suspect contain mines to aid in deduction.
- The game is won when all non-mine cells are uncovered and all mines are correctly flagged.

## Features:
- Variable grid size and number of mines.
- Safe first click guaranteeing the first cell uncovered is not a mine.
- Recursive uncovering of adjacent non-mine cells for faster gameplay.
