from src.triangle import solve
from src.interfaces import IUserInterface, INotifier
from src.database import TriangleDatabase


class TriangleController:
    def __init__(self, ui: IUserInterface, db: TriangleDatabase, notifier: INotifier):
        self.ui = ui
        self.db = db
        self.notifier = notifier

    def process(self):
        # 1. Запрос данных у пользователя
        a, b, c = self.ui.get_triangle_sides()

        # 2. Проверка в БД (Rightarrow)
        db_record = self.db.get_record(a, b, c)

        if db_record:
            # Если есть в БД, берем оттуда
            t_type, error_msg = db_record
        else:
            # Если нет - считаем и сохраняем
            t_type, coords = solve(a, b, c)
            # Формируем сообщение об ошибке (если треугольник не построился)
            error_msg = ""
            if t_type == "не треугольник" or t_type == "":
                error_msg = f"Ошибка построения. Координаты: {coords}"

            self.db.add_record(a, b, c, t_type, error_msg)

        # 3. Отправка данных на внешний сервер
        result_message = f"Треугольник со сторонами {a}, {b}, {c}: тип={t_type}"
        self.notifier.send_result(result_message)

        # 4. Возврат результата
        return t_type, error_msg