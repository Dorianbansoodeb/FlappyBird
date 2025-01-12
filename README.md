Dorian Bansoodeb FlappyBird Game

Welcome to a fresh take on the classic Flappy Bird game! This version stands out with enhanced visuals, unique gameplay mechanics, and a variety of features designed to keep you engaged. Whether you're looking to customize your bird, challenge friends on the leaderboard, or enjoy dynamic obstacle challenges, this game has something for everyone.

Features

Physics-Based Gameplay:

Gravity

Jump mechanics

Collision detection

Interactive Menu:

Start game

Change skins

View leaderboard

Share score

Exit game

Custom Skins:

Choose from a selection of bird skins.

Leaderboard:

Tracks high scores and displays them in a sorted list.

Backgrounds and Themes:

Multiple backgrounds for gameplay and menus.

Audio Effects:

Jump and death sounds.

Dynamic Obstacle Generation:

Randomized gap height and position.

Prerequisites

Before running the game, ensure you have the following installed:

Python 3.8 or higher

Required libraries (install via pip):

pygame

Installation

Clone the repository:

Navigate to the project directory:

cd flappybird-game

Install the dependencies:

pip install -r requirements.txt

Ensure the following assets are present in the working directory:

Audio:

jump_sound.mp3

death_sound.mp3

Images:

play_button.png

exit_button.png

retry_button.png

menu_button.png

lb_button.png

left_button.png

right_button.png

select_button.png

skins_button.png

share_button.png

Bird_1.png, Bird_2.png, Bird_3.png

g_brick.png

getready.png

press_space.png

gameover.png

score_button.png

lb_bg.png

text_box.png

bg_main.png, bg_play.png, bg_dead.png

Create a blank leaderboard file if not present:

touch leaderboard.txt

Running the Game

Execute the following command to start the game:

python main.py

Usage

Controls:

SPACE: Jump

ESC: Quit

Arrow Keys (Left/Right): Navigate skins

Menu Navigation:

Play: Start a new game.

Skins: Choose a different bird skin.

Leaderboard: View top scores.

Share: Submit your score to the leaderboard.

Exit: Quit the game.

File Structure

flappybird-game/
├── main.py                 # Main script
├── requirements.txt        # Dependencies
├── leaderboard.txt         # Leaderboard file
├── assets/                 # All image and sound assets
│   ├── images/             # Image files
│   ├── sounds/             # Sound files
└── README.md               # Documentation

Notes

Ensure all assets are located in the correct directories.

Adjust volume or modify assets as needed by editing main.py.

License

This project is licensed under the MIT License. See the LICENSE file for details.


