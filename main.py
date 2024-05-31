# main.py
from fire_model import ForestFireModel
from fire_visualization import ForestFireVisualization
from pymongo import MongoClient

def main():
    # Параметри моделі
    size = 50  # Розмір лісу
    p_tree = 0.7  # Ймовірність наявності дерева в клітині
    p_burn = 0.1  # Ймовірність загоряння незайманої клітини
    t_burn = 15    # Час горіння клітини
    frames = 100  # Кількість кадрів анімації

    # Підключення до MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['forest_fire']
    collection = db['simulation_results']

    # Створення та ініціалізація моделі
    model = ForestFireModel(size, p_burn, t_burn, collection)
    model.initialize(p_tree)

    # Створення об'єкту візуалізації та відображення анімації
    visualization = ForestFireVisualization(model, frames)
    visualization.animate()

if __name__ == "__main__":
    main()
