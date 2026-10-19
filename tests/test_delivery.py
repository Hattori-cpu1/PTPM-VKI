import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Delivery import calculate_delivery_cost

class TestDelivery(unittest.TestCase):

    # 1. Обычная посылка (Базовый расчет)
    def test_normal_delivery(self):
        # Вес: 1кг, Расстояние: 10км -> (200 + 10*5) = 250
        cost, date = calculate_delivery_cost(1.0, 10, "обычный")
        self.assertEqual(cost, 250)

    # 2. Весовые коэффициенты
    def test_weight_coefficient_mid(self):
        # Вес: 6кг (>5 но <20), Расстояние: 10км -> (200 + 50) * 1.2 = 300
        cost, _ = calculate_delivery_cost(6.0, 10, "обычный")
        self.assertEqual(cost, 300)

    def test_weight_coefficient_high(self):
        # Вес: 20кг (>=20), Расстояние: 10км -> (200 + 50) * 1.5 = 375
        cost, _ = calculate_delivery_cost(20.0, 10, "обычный")
        self.assertEqual(cost, 375)

    # 3. Типы посылок
    def test_fragile_package(self):
        # Вес: 1кг, Расстояние: 10км, хрупкий -> 250 + 300 = 550
        cost, _ = calculate_delivery_cost(1.0, 10, "хрупкий")
        self.assertEqual(cost, 550)

    def test_dangerous_package(self):
        # Вес: 1кг, Расстояние: 10км, опасный -> 250 + 1000 = 1250
        cost, _ = calculate_delivery_cost(1.0, 10, "опасный")
        self.assertEqual(cost, 1250)

    # 4. Валидация (Ошибки)
    def test_invalid_type(self):
        cost, date = calculate_delivery_cost(1.0, 10, "стекло")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_too_heavy(self):
        cost, _ = calculate_delivery_cost(55.0, 10, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_too_light(self):
        cost, _ = calculate_delivery_cost(0.05, 10, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_too_far(self):
        cost, _ = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)

    # 5. Время доставки
    def test_delivery_date_standard(self):
        # 1500км -> 1500 // 500 = 3 дня. 2026-09-03 + 3 = 2026-09-06
        _, date = calculate_delivery_cost(1.0, 1500, "обычный")
        self.assertEqual(date, "2026-09-06")



    # БАГ 1: Экспресс должен быть дороже, а не дешевле
    def test_express_cost_bug(self):
        # Обычная 250 руб. Экспресс по логике кода: 250 * 0.5 = 125 руб.
        # Это баг (экспресс не может быть дешевле обычной).
        cost, _ = calculate_delivery_cost(1.0, 10, "обычный", is_express=True)
        self.assertEqual(cost, 125) # Тест ПРОЙДЕТ, показывая текущее (ошибочное) поведение
        # Если исправить, тут нужно ожидать 375 (250 * 1.5) или 250 + 500

    # БАГ 2: Экспресс доставка на короткие дистанции занимает 0 дней
    def test_express_time_bug(self):
        # 100км -> 1 день. Экспресс: 1 // 2 = 0 дней.
        # Дата не сдвигается: 2026-09-03
        _, date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-03") # Баг: дата отправки и доставки совпадают!
        # Если исправить max(1, days // 2), дата должна быть хотя бы следующей

    # БАГ 3: Округление int() обрезает копейки (рубли), а не округляет
    def test_int_truncation_bug(self):
        # 1кг, 11км, экспресс: (200 + 55) * 0.5 = 127.5 руб.
        # int(127.5) вернет 127, хотя должно быть 128 (или 127.5)
        cost, _ = calculate_delivery_cost(1.0, 11, "обычный", is_express=True)
        self.assertEqual(cost, 127) # Баг: отбрасывание дробной части

if __name__ == "__main__":
    unittest.main()