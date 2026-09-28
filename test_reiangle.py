import unittest

from triangle import (
    solve, EQUILATERAL, ISOSCELES, SCALENE, NOT_TRIANGLE, INVALID,
)


class TestTriangle(unittest.TestCase):

    def _check_box(self, coords):
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_equilateral(self):
        t, c = solve("3", "3", "3")
        self.assertEqual(t, EQUILATERAL)
        self._check_box(c)

    def test_isosceles(self):
        t, c = solve("5", "5", "6")
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

    def test_not_triangle(self):
        t, c = solve("1", "2", "10")
        self.assertEqual(t, NOT_TRIANGLE)
        self.assertEqual(c, [(-1, -1)] * 3)

    def test_non_numeric(self):
        t, c = solve("abc", "2", "3")
        self.assertEqual(t, INVALID)
        self.assertEqual(c, [(-2, -2)] * 3)

    def test_empty_string(self):
        t, c = solve("", "", "")
        self.assertEqual(t, INVALID)
        self.assertEqual(c, [(-2, -2)] * 3)

    def test_negative(self):
        _, c = solve("-1", "2", "3")
        self.assertEqual(c, [(-1, -1)] * 3)

    def test_zero(self):
        _, c = solve("0", "2", "3")
        self.assertEqual(c, [(-1, -1)] * 3)


if __name__ == "__main__":
    unittest.main()