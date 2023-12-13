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
1. Number/clue:![Tile1](https://github.com/Louiselulul/MineSweeper/assets/109748663/31da1ab4-58c7-420d-8afa-a8cba33a0510)
2. Mine: ![TileMine](https://github.com/Louiselulul/MineSweeper/assets/109748663/7af0097c-4199-4184-8f60-4d65edcbedf6)
4. Flag: ![TileFlag](https://github.com/Louiselulul/MineSweeper/assets/109748663/8f647b85-3005-4507-a506-a3105ccb6f35)
5. If player hits a mine, it explodes: ![TileExploded](https://github.com/Louiselulul/MineSweeper/assets/109748663/96e3aa61-cbe2-45be-961d-3c058b67c4cd)
6. If player mis-placed a flag, this will show up when player hits a mine and ends the game: ![TileNotMine](https://github.com/Louiselulul/MineSweeper/assets/109748663/2cb1dbee-f106-43f1-b18e-c34a61678816)
7. Unknown/un-clicked tile:![TileUnknown](https://github.com/Louiselulul/MineSweeper/assets/109748663/b5fe1cf0-413c-4c7d-848f-8a3115578f0a)
8. Blank/background tile: ![TileEmpty](https://github.com/Louiselulul/MineSweeper/assets/109748663/b1523f2a-4e9f-49ee-83e1-4c4febb22fc1)

## User Interface
Here shows the user interface of our game
<p align="center">
  <img src="user_interface_example.jpg" width="350" title="Minesweeper Gameplay">
  <br>
  <em>Figure 1: Minesweeper Gameplay Screenshot</em>
</p>

When player wins:
![wub](https://github.com/Louiselulul/MineSweeper/assets/109748663/9648c821-9b46-4829-b2ac-7e4ef83163a9)

When player loses:
![lose](https://github.com/Louiselulul/MineSweeper/assets/109748663/7883a577-6525-4fe7-96df-74dac524eb39)

## Installation

Clone the GitHub repository:

```bash
git clone https://github.com/Louiselulul/MineSweeper.git
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

## Pygame Installation Issue Solution
NOTE: This game requires pygame module.
Note that python version greater than 3.10 (e.g 3.11) is incompatible with pygame module auto-installation within pycharm. If you encounter an error message saying installation failure, this might be due to your python version. You can try the following steps (This works if you downloaded pycharm through anaconda):

First, check your interpreter version:
- Open pycharm --> File --> Settings --> Project: --> Python interpreter

Now, you may see your python version directly next to "python interpreter". However, if it says "anaconda3" and you don't see your python version:
- Open Andaconda Prompt, type the command "python".
- Optional: to get a list of all installed packages and verify their version, type "conda list"
- To exist, type "quit()"

Now, if you see that you have python 3.11, then the installation error is probably because of it. You can try 2 things:
1. [Directly download pygame without changing your python vesrion] Open Anaconda Prompt, type ```bash pip install pygame ``` to install pygame, type "pip show pygame" to verify installation.
2. [Changing your current python version to older ones]Click the down-arrow next to python interpreter, if you have project that used older python version on your computer, you should see other interpreters showing earlier python version. You can directly choose them, and now your currently project's interpreter will be changed, now try installing pygame again.
   
## Contributors

- [CHEN Xiaojun (AivlysCxx)](https://github.com/AivlysCxx): Define game's logic and data structure, such as the tiles placement and game board functionalities. 
- [LU Yuqing (Louiselulul)](https://github.com/Louiselulul): Define the game environment, user interaction, and the main game loop, such as PygameGame Class.




