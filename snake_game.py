import pygame
import random
import sys
from snake_ai import QLearningAgent


WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.reset_game()
        self.ai_agent = QLearningAgent()
        self.ai_agent.load_q_table()  
        self.ai_mode = False



    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self._generate_food()
        self.score = 0

    def _generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def get_state(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        food_dx_dir = 1 if food_x > head_x else 0
        food_dy_dir = 1 if food_y > head_y else 0

        danger_left = int((head_x - 1, head_y) in self.snake or head_x == 0)
        danger_right = int((head_x + 1, head_y) in self.snake or head_x == GRID_WIDTH - 1)
        danger_up = int((head_x, head_y - 1) in self.snake or head_y == 0)
        danger_down = int((head_x, head_y + 1) in self.snake or head_y == GRID_HEIGHT - 1)

        return (food_dx_dir, food_dy_dir, danger_left, danger_right, danger_up, danger_down)



    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ai_mode = not self.ai_mode
                        if not self.ai_mode:
                            self.ai_agent.save_q_table()
                    elif not self.ai_mode:
                        if event.key == pygame.K_UP and self.direction != (0, 1):
                            self.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.direction = (1, 0)

            if self.ai_mode:
                state = self.get_state()
                action = self.ai_agent.get_action(state)
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                proposed_direction = directions[action]
                opposite_direction = (-self.direction[0], -self.direction[1])
                if proposed_direction != opposite_direction:
                    self.direction = proposed_direction

            old_distance = manhattan_distance(self.snake[0], self.food)

            head_x, head_y = self.snake[0]
            new_head = (
                (head_x + self.direction[0]) % GRID_WIDTH,
                (head_y + self.direction[1]) % GRID_HEIGHT
            )

            if new_head in self.snake:
                reward = -50  
                if self.ai_mode:
                    next_state = self.get_state()
                    self.ai_agent.update_q_table(state, action, reward, next_state)
                self.reset_game()
                continue

            new_distance = manhattan_distance(new_head, self.food)

            self.snake.insert(0, new_head)

            if new_head == self.food:
                self.food = self._generate_food()
                self.score += 1
                reward = 20
            else:
                self.snake.pop()
                reward = 1 if new_distance < old_distance else -1

            if self.ai_mode:
                next_state = self.get_state()
                self.ai_agent.update_q_table(state, action, reward, next_state)

            self.screen.fill(BLACK)
            for segment in self.snake:
                pygame.draw.rect(self.screen, GREEN,
                                (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, RED,
                            (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            ai_text = self.font.render(f"AI: {'ON' if self.ai_mode else 'OFF'}", True,
                                       GREEN if self.ai_mode else RED)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(ai_text, (10, 40))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.ai_agent.save_q_table() 

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
