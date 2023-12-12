# MineSweeper

## Project Introduction:
- Our project implements the classic game of Minesweeper in Python. The goal is to uncover all cells without mines.

## Gameplay:
- The player starts by uncovering a cell. 
- If the cell contains a mine, the game ends.
- If the cell does not contain a mine, it displays a number indicating how many adjacent cells contain mines.
- The player uses the number clues on each block to infer which neighboring cells are safe to open.
- The player can place flags on cells they suspect contain mines to aid in deduction.
- The game is won when all non-mine cells are uncovered and all mines are correctly flagged.


## Features
- **Safe First Click:** Ensures the first cell clicked is never a mine.
- **Recursive Uncovering:** Automatically uncovers adjacent cells when a safe cell is revealed.
- **Flagging Capability:** Players can flag cells they suspect contain mines.
- **Console-Based Interface:** Easy-to-use interface for game interaction.
- **Timer:** Tracks how long it takes to solve the board.

## User Interface
here shows the user interface of our game
<p align="center">
  <img src="user_interface_example.jpg" width="350" title="Minesweeper Gameplay">
  <br>
  <em>Figure 1: Minesweeper Gameplay Screenshot</em>
</p>


