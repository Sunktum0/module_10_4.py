import threading
import random
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number  # Номер стола
        self.guest = None  # Гость за столом

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Имя гостя

    def run(self):
        # Гость "сидит" за столом от 3 до 10 секунд
        eating_time = random.randint(3, 10)
        time.sleep(eating_time)

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Очередь гостей
        self.tables = tables  # Список столов

    def guest_arrival(self, *guests):
        for guest in guests:
            # Проверяем, есть ли свободный стол
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:  # Если есть свободный стол
                free_table.guest = guest  # Сажаем гостя за стол
                guest.start()  # Запускаем поток
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:  # Если свободных столов нет
                self.queue.put(guest)  # Гость в очередь
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():  # Если гость закончил приём пищи
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

                    if not self.queue.empty():  # Если очередь не пуста
                        next_guest = self.queue.get()  # Берем следующего гостя из очереди
                        table.guest = next_guest  # Садим его за стол
                        next_guest.start()  # Запускаем поток
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            time.sleep(1)  # Ожидаем перед проверкой состояния столов и очереди

# Пример использования
if __name__ == "__main__":
    # Создание столов
    tables = [Table(i) for i in range(1, 6)]  # 5 столов
    cafe = Cafe(*tables)  # Создание кафе с этими столами

    # Создание гостей
    guests = [Guest(f"Гость {i}") for i in range(1, 11)]  # 10 типов гостей

    # Прибытие гостей
    cafe.guest_arrival(*guests)

    # Обслуживание гостей
    cafe.discuss_guests()