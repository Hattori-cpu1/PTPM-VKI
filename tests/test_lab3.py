import unittest
from unittest.mock import Mock, patch
from src.controller import TriangleController
from src.database import TriangleDatabase
from src.interfaces import ConsoleUserInterface, EmailNotifier


class TestDatabaseLayer(unittest.TestCase):
    """Тестируем изолированно класс базы данных (Класс b)"""

    def setUp(self):
        # Используем БД в оперативной памяти для каждого теста
        self.db = TriangleDatabase(":memory:")

    def test_db_add_and_get(self):
        self.db.add_record("3", "4", "5", "разносторонний", "")
        record = self.db.get_record("3", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "разносторонний")

    def test_db_get_missing_record(self):
        record = self.db.get_record("9", "9", "9")
        self.assertIsNone(record)

    def test_db_delete_record(self):
        self.db.add_record("3", "3", "3", "равносторонний", "")
        self.db.delete_record("3", "3", "3")
        record = self.db.get_record("3", "3", "3")
        self.assertIsNone(record)


class TestInterfacesWithMocks(unittest.TestCase):
    """Тестируем классы интерфейсов с помощью подмены ввода/вывода"""

    @patch('builtins.input', side_effect=['5', '5', '6'])
    def test_console_ui_mock_input(self, mock_input):
        ui = ConsoleUserInterface()
        a, b, c = ui.get_triangle_sides()
        self.assertEqual((a, b, c), ('5', '5', '6'))
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.print')
    def test_email_notifier_mock_print(self, mock_print):
        notifier = EmailNotifier()
        notifier.send_result("Тестовое сообщение")
        mock_print.assert_called_once_with("[Email Server] Отправлено сообщение: Тестовое сообщение")


class TestControllerIntegration(unittest.TestCase):
    """
    ИНТЕГРАЦИОННЫЕ ТЕСТЫ (Класс e + БД + Заглушки).
    Проверяем сквозной сценарий работы контроллера.
    """

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

        # Создаем заглушки для UI и Notifier
        self.mock_ui = Mock()
        self.mock_notifier = Mock()

        # Инициализируем контроллер, подсовывая ему реальную БД и заглушки
        self.controller = TriangleController(
            ui=self.mock_ui,
            db=self.db,
            notifier=self.mock_notifier
        )

    # ИНТЕГРАЦИОННЫЙ ТЕСТ 1: Успешный расчет и сохранение в БД (Cache Miss)
    def test_integration_new_triangle_calculates_and_saves(self):
        # Настраиваем заглушку: пользователь ввел 3, 4, 5
        self.mock_ui.get_triangle_sides.return_value = ("3", "4", "5")

        # Запускаем бизнес-логику
        t_type, error = self.controller.process()

        # 1. Проверяем, что контроллер вернул правильный тип
        self.assertEqual(t_type, "разносторонний")
        # 2. Проверяем, что запись реально появилась в БД
        db_record = self.db.get_record("3", "4", "5")
        self.assertEqual(db_record[0], "разносторонний")
        # 3. Проверяем, что уведомление ушло на "сервер" (вызвался Mock)
        self.mock_notifier.send_result.assert_called_once()

    # ИНТЕГРАЦИОННЫЙ ТЕСТ 2: Кэширование (Cache Hit). Берем из БД, не считаем.
    @patch('src.controller.solve')
    def test_integration_existing_triangle_takes_from_db(self, mock_solve):
        # Заранее кладем запись в БД
        self.db.add_record("3", "3", "3", "равносторонний", "")

        # Пользователь вводит те же данные
        self.mock_ui.get_triangle_sides.return_value = ("3", "3", "3")

        t_type, error = self.controller.process()

        # ГЛАВНАЯ ПРОВЕРКА: математическая функция solve НЕ должна вызываться
        mock_solve.assert_not_called()
        self.assertEqual(t_type, "равносторонний")
        self.mock_notifier.send_result.assert_called_once()

    # ИНТЕГРАЦИОННЫЙ ТЕСТ 3: Обработка "не треугольника" и сохранение ошибки
    def test_integration_invalid_triangle_saves_error(self):
        self.mock_ui.get_triangle_sides.return_value = ("1", "2", "10")

        t_type, error = self.controller.process()

        self.assertEqual(t_type, "не треугольник")
        self.assertIn("Ошибка", error)

        # Проверяем, что ошибка сохранилась в БД
        db_record = self.db.get_record("1", "2", "10")
        self.assertIn("Ошибка", db_record[1])
        self.mock_notifier.send_result.assert_called_once()

    # ИНТЕГРАЦИОННЫЙ ТЕСТ 4: Сквозной тест с подменой реального ввода (patch)
    @patch('builtins.input', side_effect=['6', '6', '6'])
    def test_full_flow_with_real_ui_and_mocked_input(self, mock_input):
        # Заменяем заглушку UI на реальный класс ConsoleUserInterface
        real_ui = ConsoleUserInterface()
        controller = TriangleController(ui=real_ui, db=self.db, notifier=self.mock_notifier)

        t_type, error = controller.process()

        self.assertEqual(t_type, "равносторонний")
        self.mock_notifier.send_result.assert_called_once()


if __name__ == "__main__":
    unittest.main()