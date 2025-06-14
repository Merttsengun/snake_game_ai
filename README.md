# Snake AI Game

This project is a classic Snake game where the snake is controlled by an AI agent trained using Q-learning. The game is built using Python and Pygame, and the AI gradually learns to play better through reinforcement learning.

## Features

- Classic Snake game with grid-based movement.
- AI mode using Q-learning algorithm.
- Manual control mode (arrow keys).
- Persistent Q-table saving for continuous learning.
- Adjustable FPS for faster AI training.

## How to Run

1. Clone or download this repository.

2. Install required packages:
pip install pygame numpy

3. Run the game:
python snake_game.py


## Controls

- Arrow Keys: Control the snake manually.
- Space: Toggle AI mode ON/OFF.
- X (Window close): Exits and saves the Q-table.

## File Descriptions

- `snake_game.py` – Main game loop, graphics, input, and game logic.
- `snake_ai.py` – Q-learning AI agent (training, prediction, and saving).
- `q_table.npy` – The saved Q-table storing the AI's learned behavior.
- `README.md` – Project overview and setup instructions.

## Notes

- The AI trains over time by learning from game outcomes.
- You can increase `FPS` in `snake_game.py` to accelerate training.
- Closing the game saves the current AI progress automatically.

---

Feel free to improve or experiment with the AI logic for better performance! 
