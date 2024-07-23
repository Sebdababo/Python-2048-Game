# Python 2048 Game

## Description

This project is a Python implementation of the popular 2048 game, featuring a graphical user interface built using the Tkinter library. The game involves sliding numbered tiles on a grid to combine them and create a tile with the number 2048. 

## Features

- Classic 2048 gameplay with a 4x4 grid
- Smooth animations and a visually appealing interface
- Tracks current score and high score
- Option to continue playing after reaching 2048
- Reset game functionality
- Simple and intuitive controls using arrow keys

## Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/Sebdababo/Python-2048-Game.git
    cd Python-2048-Game
    ```

2. **Install the required libraries:**
    ```
    pip install -r requirements.txt
    ```

3. **Run the game:**
    ```
    python 2048_game.py
    ```

## Usage

When you run the game, a window will open displaying a 4x4 grid. Use the arrow keys to slide the tiles in the corresponding direction:

- **Left Arrow Key:** Slide tiles left
- **Right Arrow Key:** Slide tiles right
- **Up Arrow Key:** Slide tiles up
- **Down Arrow Key:** Slide tiles down
- **R Key:** Reset the game

### Gameplay

- **Objective:** Combine tiles with the same number to create a tile with the number 2048.
- **Score:** Your score increases each time you combine tiles.
- **Winning:** When you create a tile with the number 2048, you win! You can choose to continue playing to reach higher numbers.
- **Game Over:** The game ends when there are no valid moves left.

## Data Persistence

The game keeps track of your high score during the session, but it does not save it between sessions. Future versions may include persistent high score tracking.
