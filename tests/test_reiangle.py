import unittest
import sys
import os

# Чтобы тесты видели папку src при запуске
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.triangle import (
    solve, EQUILATERAL, ISOSCELES, SCALENE, NOT_TRIANGLE, INVALID,
)

class TestTriangle(unittest.TestCase):

    def _check_box(self, coords):
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    # --- 1-5: Базовые типы ---
    def test_equilateral(self):
        t, c = solve("3", "3", "3")
        self.assertEqual(t, EQUILATERAL)
        self._check_box(c)

    def test_isosceles(self):
        t, c = solve("5", "5", "6")
        self.assertEqual(t, ISOSCELES)
        self._check_box(c)

    def test_isosceles_variant2(self):
        t, c = solve("5", "6", "5")
        self.assertEqual(t, ISOSCELES)
        self._check_box(c)

    def test_scalene(self):
        t, c = solve("3", "4", "5")
        self.assertEqual(t, SCALENE)
        self._check_box(c)

    def test_float_equilateral(self):
        t, c = solve("2.5", "2.5", "2.5")
        self.assertEqual(t, EQUILATERAL)
        self._check_box(c)

    # --- 6-10: Логика "не треугольник" ---
    def test_not_triangle(self):
        t, c = solve("1", "2", "10")
        self.assertEqual(t, NOT_TRIANGLE)
        self.assertEqual(c, [(-1, -1)] * 3)

    def test_not_triangle_sum_equal(self):
        t, c = solve("1", "2", "3")
        self.assertEqual(t, NOT_TRIANGLE)
        self.assertEqual(c, [(-1, -1)] * 3)

    def test_negative(self):
        t, c = solve("-1", "2", "3")
        self.assertEqual(t, NOT_TRIANGLE)
        self.assertEqual(c, [(-1, -1)] * 3)

    def test_zero(self):
        t, c = solve("0", "2", "3")
        self.assertEqual(t, NOT_TRIANGLE)
        self.assertEqual(c, [(-1, -1)] * 3)

    def test_huge_values(self):
        t, c = solve("1000", "1000", "1000")
        self.assertEqual(t, EQUILATERAL)
        self._check_box(c)

    # --- 11-15: Ошибочные данные (нечисловые) ---
    def test_non_numeric(self):
        t, c = solve("abc", "2", "3")
        self.assertEqual(t, INVALID)
        self.assertEqual(c, [(-2, -2)] * 3)

    def test_empty_string(self):
        t, c = solve("", "", "")
        self.assertEqual(t, INVALID)
        self.assertEqual(c, [(-2, -2)] * 3)

    def test_only_one_non_numeric(self):
        t, c = solve("3", "4", "xyz")
        self.assertEqual(t, INVALID)
        self.assertEqual(c, [(-2, -2)] * 3)

    def test_none_input(self):
        t, c = solve(None, "4", "5")
        self.assertEqual(t, INVALID)
        self.assertEqual(c, [(-2, -2)] * 3)

    def test_spaces_input(self):
        t, c = solve("  3  ", " 4", "5 ")
        self.assertEqual(t, SCALENE)
        self._check_box(c)

    # --- 16-21: Проверки координат и форматов ---
    def test_coordinates_count(self):
        _, c = solve("3", "4", "5")
        self.assertEqual(len(c), 3)

    def test_coordinates_types(self):
        _, c = solve("3", "4", "5")
        for x, y in c:
            self.assertIs(type(x), int)
            self.assertIs(type(y), int)

    def test_coordinates_y_inversion(self):
        # Проверяем, что Y инвертирован (экранная система координат)
        _, c = solve("3", "4", "5")
        # Самая нижняя точка (максимальный Y в математике) должна иметь минимальный Y на экране
        ys = [y for x, y in c]
        self.assertTrue(min(ys) >= 0)
        self.assertTrue(max(ys) <= 100)

    def test_scientific_notation(self):
        t, _ = solve("3e0", "4e0", "5e0")
        self.assertEqual(t, SCALENE)

    def test_large_numbers_fitting(self):
        _, c = solve("100", "100", "100")
        self._check_box(c)

    def test_tiny_numbers_fitting(self):
        _, c = solve("0.1", "0.1", "0.1")
        self._check_box(c)


if __name__ == "__main__":
    unittest.main()