import logging
import os
import sys

from triangle import solve

LOG_DIR = "Logs"
LOG_FILE = os.path.join(LOG_DIR, "file_txt.log")
LOG_FORMAT = "%(asctime)s | [%(levelname)-7s] | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging() -> None:

    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
    )
    logging.info("Логгер успешно сконфигурирован")


def read_line(prompt: str) -> str:

    try:
        return input(prompt)
    except EOFError:
        return ""


def process_one_triangle() -> bool:

    raw_a = read_line("Введите сторону A (Enter — выход): ").strip()

    if raw_a == "":
        return False

    raw_b = read_line("Введите сторону B: ").strip()
    raw_c = read_line("Введите сторону C: ").strip()

    logging.info(f"Запрос: A={raw_a!r}, B={raw_b!r}, C={raw_c!r}")

    triangle_type, coordinates = solve(raw_a, raw_b, raw_c)

    print(f"Тип треугольника: {triangle_type}")
    print(f"Координаты вершин: {coordinates}")
    print("-" * 40)

    logging.info(
        f"Успешный запрос. Результат: тип={triangle_type!r}, координаты={coordinates}"
    )
    return True


def main() -> None:
    configure_logging()
    logging.info("Приложение запущено")
    print("Введите стороны треугольника. Для выхода — пустая строка (просто Enter).")

    try:
        while True:
            try:
                if not process_one_triangle():
                    break
            except  Exception as exc:

                logging.exception(f"Неуспешный запрос. Ошибка: {exc}")
                print("Ошибка при обработке. Попробуйте снова.")
                print("-" * 40)
    except KeyboardInterrupt:

        logging.info("Получен KeyboardInterrupt (Ctrl+C)")
        print("\nВыход по Ctrl+C.")
    finally:
        logging.info("Приложение завершило работу")


if __name__ == "__main__":
    main()