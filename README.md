# MineSweeper

## Project Introduction:
- Our project implements the classic game of Minesweeper in Python. The goal is to uncover all cells without mines.

## Gameplay:
- The player starts by uncovering a cell. 
- If the cell contains a mine, the game ends.
- If the cell does not contain a mine, it displays a number indicating how many adjacent cells contain mines.
- The player uses the number clues on each block to infer which neighboring cells are safe to open.
- The player can place flags on cells they suspect contain mines to aid in deduction (right-click to place a flag, right-click again to unplace a flag)
- The game is won when all non-mine cells are uncovered and all mines are correctly flagged.

## Features
- **Safe First Click:** Ensures the first cell clicked is never a mine.
- **Recursive Uncovering:** Automatically uncovers adjacent cells when a safe cell is revealed.
- **Flagging Capability:** Players can flag cells they suspect contain mines.
- **Console-Based Interface:** Easy-to-use interface for game interaction.
- **Timer:** Tracks how long it takes to solve the board.

## Types of cell/tile:
1. Number/clue tile:![Tile1](https://github.com/Louiselulul/MineSweeper/assets/109748663/31da1ab4-58c7-420d-8afa-a8cba33a0510)

2. 

## User Interface
Here shows the user interface of our game
<p align="center">
  <img src="user_interface_example.jpg" width="350" title="Minesweeper Gameplay">
  <br>
  <em>Figure 1: Minesweeper Gameplay Screenshot</em>
</p>

## Installation

Clone the GitHub repository:

```bash
git clone https://github.com/Louiselulul/MineSweeper.git
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

## Contributors

- [CHEN Xiaojun (AivlysCxx)](https://github.com/AivlysCxx): Define game's logic and data structure, such as the tiles placement and game board functionalities. 
- [LU Yuqing (Louiselulul)](https://github.com/Louiselulul): Define the game environment, user interaction, and the main game loop, such as PygameGame Class.




