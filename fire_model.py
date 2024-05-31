import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

class ForestFireModel:
    def __init__(self, size, p_burn, t_burn, collection):
        self.size = size
        self.p_burn = p_burn
        self.t_burn = t_burn
        self.grid = np.zeros((size, size))  # 0: незаймана, 1: горить, 2: згоріла
        self.running = False
        self.collection = collection

    def initialize(self, p_tree):
        # Ініціалізуємо початковий стан лісу, де деякі клітини мають дерева
        self.grid = np.random.choice([0, 1], size=(self.size, self.size), p=[1 - p_tree, p_tree])

    def step(self):
        new_grid = np.copy(self.grid)

        # Використовуємо ThreadPoolExecutor для паралельного виконання
        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(self.size):
                for j in range(self.size):
                    futures.append(executor.submit(self.process_cell, i, j, new_grid))

            for future in as_completed(futures):
                pass  # Виконання завершено для кожної клітинки

        self.grid = new_grid
        # Записуємо результат в MongoDB
        self.save_to_db()

    def process_cell(self, i, j, new_grid):
        if self.grid[i, j] == 0:  # незаймана клітина
            if np.random.random() < self.p_burn:
                if self.check_burning_neighbors(i, j):
                    new_grid[i, j] = 1  # клітина загорілася
        elif self.grid[i, j] == 1:  # горить
            if np.random.random() < 1 / self.t_burn:
                new_grid[i, j] = 2  # клітина згоріла

    def check_burning_neighbors(self, i, j):
        # Перевіряємо, чи є поруч горячі клітини
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        for ni, nj in neighbors:
            if 0 <= ni < self.size and 0 <= nj < self.size and self.grid[ni, nj] == 1:
                return True
        return False

    def save_to_db(self):
        grid_list = self.grid.tolist()  # Перетворюємо numpy array у список
        self.collection.insert_one({"grid": grid_list})