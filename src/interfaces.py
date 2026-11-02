from abc import ABC, abstractmethod


class IUserInterface(ABC):
    @abstractmethod
    def get_triangle_sides(self) -> tuple[str, str, str]:

        pass

# Класс сторонней зависимости (Class d)
class INotifier(ABC):
    @abstractmethod
    def send_result(self, result: str) -> None:

        pass




class ConsoleUserInterface(IUserInterface):
    def get_triangle_sides(self) -> tuple[str, str, str]:
        a = input("Введите сторону A: ")
        b = input("Введите сторону B: ")
        c = input("Введите сторону C: ")
        return a, b, c

class EmailNotifier(INotifier):
    def send_result(self, result: str) -> None:

        print(f"[Email Server] Отправлено сообщение: {result}")