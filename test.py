# test.py
import unittest
import numpy as np
import mongomock
from fire_model import ForestFireModel

class TestForestFireModel(unittest.TestCase):

    def setUp(self):
        # Налаштування початкових умов для тестів
        self.size = 10  # Розмір сітки
        self.p_burn = 0.1  # Ймовірність згоряння дерева
        self.t_burn = 15  # Час горіння дерева
        self.collection = mongomock.MongoClient().db.collection  # Імітація MongoDB колекції
        self.model = ForestFireModel(self.size, self.p_burn, self.t_burn, self.collection)  # Ініціалізація моделі лісової пожежі

    def test_initialize(self):
        # Тестування методу initialize
        p_tree = 0.7  # Ймовірність засадження дерева
        self.model.initialize(p_tree)  # Ініціалізація сітки
        tree_count = np.sum(self.model.grid == 1)  # Підрахунок кількості дерев
        empty_count = np.sum(self.model.grid == 0)  # Підрахунок кількості порожніх клітин
        total_count = tree_count + empty_count  # Загальна кількість клітин
        self.assertEqual(total_count, self.size * self.size)  # Перевірка, що кількість клітин відповідає розміру сітки
        self.assertAlmostEqual(tree_count / total_count, p_tree, delta=0.1)  # Перевірка, що частка дерев відповідає заданій ймовірності

    def test_step(self):
        # Тестування методу step
        p_tree = 0.7  # Ймовірність засадження дерева
        self.model.initialize(p_tree)  # Ініціалізація сітки
        initial_grid = np.copy(self.model.grid)  # Збереження початкового стану сітки
        self.model.step()  # Виконання одного кроку моделі
        self.assertEqual(self.model.grid.shape, (self.size, self.size))  # Перевірка, що розмір сітки не змінився
        self.assertNotEqual(np.sum(self.model.grid == 1), np.sum(initial_grid == 1))  # Перевірка, що кількість дерев змінилася
        self.assertNotEqual(np.sum(self.model.grid == 2), np.sum(initial_grid == 2))  # Перевірка, що кількість згорілих дерев змінилася

    def test_check_burning_neighbors(self):
        # Тестування методу check_burning_neighbors
        self.model.grid[0, 0] = 1  # Встановлення клітини, що горить
        self.assertTrue(self.model.check_burning_neighbors(0, 1))  # Перевірка, що сусідня клітина горить
        self.assertFalse(self.model.check_burning_neighbors(1, 1))  # Перевірка, що сусідні клітини не горять

    def test_save_to_db(self):
        # Тестування методу save_to_db
        self.model.grid[0, 0] = 1  # Встановлення клітини, що горить
        self.model.save_to_db()  # Збереження стану сітки до бази даних
        saved_record = self.collection.find_one()  # Отримання збереженого запису
        self.assertIsNotNone(saved_record)  # Перевірка, що запис існує
        self.assertIn('grid', saved_record)  # Перевірка, що сітка збережена
        self.assertEqual(saved_record['grid'][0][0], 1)  # Перевірка, що збережений стан відповідає встановленому
        self.assertEqual(saved_record['grid'][1][1], 0)  # Перевірка, що інші клітини порожні

if __name__ == '__main__':
    unittest.main()  # Запуск тестів
