# test.py
import unittest
import numpy as np
import mongomock
from fire_model import ForestFireModel

class TestForestFireModel(unittest.TestCase):

    def setUp(self):
        self.size = 10
        self.p_burn = 0.1
        self.t_burn = 15
        self.collection = mongomock.MongoClient().db.collection
        self.model = ForestFireModel(self.size, self.p_burn, self.t_burn, self.collection)

    def test_initialize(self):
        p_tree = 0.7
        self.model.initialize(p_tree)
        tree_count = np.sum(self.model.grid == 1)
        empty_count = np.sum(self.model.grid == 0)
        total_count = tree_count + empty_count
        self.assertEqual(total_count, self.size * self.size)
        self.assertAlmostEqual(tree_count / total_count, p_tree, delta=0.1)

    def test_step(self):
        p_tree = 0.7
        self.model.initialize(p_tree)
        initial_grid = np.copy(self.model.grid)
        self.model.step()
        self.assertEqual(self.model.grid.shape, (self.size, self.size))
        self.assertNotEqual(np.sum(self.model.grid == 1), np.sum(initial_grid == 1))
        self.assertNotEqual(np.sum(self.model.grid == 2), np.sum(initial_grid == 2))

    def test_check_burning_neighbors(self):
        self.model.grid[0, 0] = 1  # Клітина горить
        self.assertTrue(self.model.check_burning_neighbors(0, 1))  # Поруч клітина горить
        self.assertFalse(self.model.check_burning_neighbors(1, 1))  # Поруч клітин не горить

    def test_save_to_db(self):
        self.model.grid[0, 0] = 1  # Додамо дані до сітки
        self.model.save_to_db()
        saved_record = self.collection.find_one()
        self.assertIsNotNone(saved_record)
        self.assertIn('grid', saved_record)
        self.assertEqual(saved_record['grid'][0][0], 1)
        self.assertEqual(saved_record['grid'][1][1], 0)  # Інші клітини повинні бути 0

if __name__ == '__main__':
    unittest.main()
