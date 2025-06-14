import numpy as np
import random

class QLearningAgent:
    def __init__(self):
        
        self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 4))
        self.learning_rate = 0.1
        self.discount = 0.9
        self.epsilon = 0.15

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        next_max = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount * next_max - current_q)
        self.q_table[state][action] = new_q

    def save_q_table(self, filename="q_table.npy"):
        np.save(filename, self.q_table)

    def load_q_table(self, filename="q_table.npy"):
        try:
            self.q_table = np.load(filename)
           
            if self.q_table.shape != (2, 2, 2, 2, 2, 2, 4):
                print("Uyarı: Q-table boyutu uyumsuz, yeniden sıfırlanıyor.")
                self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 4))
        except FileNotFoundError:
            print("Q-table dosyası bulunamadı, yeni tablo oluşturuluyor.")
            self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 4))
