from __future__ import annotations

import logging
import math
from typing import List, Tuple

logger = logging.getLogger(__name__)


EQUILATERAL = "равносторонний"
ISOSCELES = "равнобедренный"
SCALENE = "разносторонний"
NOT_TRIANGLE = "не треугольник"
INVALID = ""


BOX_SIZE = 100
MARGIN = 10
EPS = 1e-9

ERROR_NUMERIC_COORD = (-1, -1)
ERROR_NON_NUMERIC_COORD = (-2, -2)

Point = Tuple[int, int]


def _parse_side(raw, name: str) -> float:

    if raw is None:
        raise ValueError(f"Сторона {name}: значение отсутствует")
    try:
        return float(str(raw).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Сторона {name}: нечисловое значение {raw!r}") from exc


def _classify(a: float, b: float, c: float) -> str:

    if a + b <= c + EPS or a + c <= b + EPS or b + c <= a + EPS:
        return NOT_TRIANGLE
    if abs(a - b) < EPS and abs(b - c) < EPS:
        return EQUILATERAL
    if abs(a - b) < EPS or abs(b - c) < EPS or abs(a - c) < EPS:
        return ISOSCELES
    return SCALENE


def _compute_coordinates(a: float, b: float, c: float) -> List[Point]:

    x_c = (b * b - a * a + c * c) / (2.0 * c)
    y_sq = b * b - x_c * x_c
    if y_sq < 0:
        y_sq = 0.0
    y_c = math.sqrt(y_sq)

    raw_points = [(0.0, 0.0), (c, 0.0), (x_c, y_c)]

    xs = [p[0] for p in raw_points]
    ys = [p[1] for p in raw_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y
    usable = BOX_SIZE - 2 * MARGIN

    scales = []
    if width > EPS:
        scales.append(usable / width)
    if height > EPS:
        scales.append(usable / height)
    scale = min(scales) if scales else 1.0

    result: List[Point] = []
    for px, py in raw_points:
        nx = MARGIN + (px - min_x) * scale
        ny = MARGIN + (py - min_y) * scale
        ny_screen = BOX_SIZE - ny  # инверсия Y для экранных координат
        result.append((int(round(nx)), int(round(ny_screen))))
    return result


def solve(raw_a, raw_b, raw_c):

    try:
        a = _parse_side(raw_a, "A")
        b = _parse_side(raw_b, "B")
        c = _parse_side(raw_c, "C")
    except ValueError as exc:
        logger.warning(f"Невалидные (нечисловые) данные: {exc}")
        return INVALID, [ERROR_NON_NUMERIC_COORD] * 3

    logger.debug(f"Числовые стороны: A={a}, B={b}, C={c}")

    if a <= 0 or b <= 0 or c <= 0:
        logger.warning(
            f"Некорректные числовые данные (не положительные): A={a}, B={b}, C={c}"
        )
        return NOT_TRIANGLE, [ERROR_NUMERIC_COORD] * 3

    triangle_type = _classify(a, b, c)
    logger.info(f"Вид треугольника: {triangle_type}")

    if triangle_type == NOT_TRIANGLE:
        return triangle_type, [ERROR_NUMERIC_COORD] * 3

    coords = _compute_coordinates(a, b, c)
    logger.debug(f"Координаты вершин (100x100): {coords}")
    return triangle_type, coords