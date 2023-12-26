from dataclasses import dataclass, field
from enum import Enum
import csv

@dataclass
class UserRole(Enum):
    READER = 0
    LIBRARIAN = 1

@dataclass
class User:
    id: int
    login: str
    password: str
    role: UserRole

@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    genre: str
    available: bool

@dataclass
class OrderStatus(Enum):
    CREATED = 0
    CONFIRMED = 1
    COMPETED = 2
@dataclass
class Order:
    id: int
    user_id: int
    book_ids: list
    status: OrderStatus = OrderStatus.CREATED
import cmd
class LibrarySystem(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.users = []
        self.books = []
        self.orders = []
        self.prompt = "Библиотека> "
        self.intro = "Добро пожаловать в систему библиотеки. Введите 'help' для просмотра доступных комманд."

    def do_exit(self, line):
        print("Покидаем библиотеку...")
        return True

    def do_add_user(self, line):
        user_id = len(self.users) + 1
        login, password, role = line.split()
        role = Role(int(role))
        user = User(user_id, login, password, role)
        self.users.append(user)
        print(f"Пользователь {user.login} был добавлен с ID {user.id}")

    def do_add_book(self, line):
        book_id = len(self.books) + 1
        title, author, description, genre, available = line.split(',')
        available = bool(available)
        book = Book(book_id, title, author, description, genre, available)
        self.books.append(book)
        print(f"Книга '{book.title}' была добавлена с ID {book.id}")

    def do_remove_book(self, book_id):
        book_id = int(book_id)
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                print(f"Книга с ID {book_id} была удалена")
                return
        print(f"Книга с  ID {book_id} не найдена")

    def do_change_book_availability(self, line):
        book_id, available = line.split()
        book_id = int(book_id)
        available = bool(available)
        for book in self.books:
            if book.id == book_id:
                book.available = available
                print(f"Значение доступа к книге с ID {book_id} было заменено на {available}")
                return
        print(f"Книга с ID {book_id} не найдена")

    def do_confirm_order(self, order_id):
        order_id = int(order_id)
        for order in self.orders:
            if order.id == order_id:
                order.status = Status.CONFIRMED
                print(f"Заказ с ID {order_id} был подтвержден")
                return
        print(f"Заказ с ID {order_id} не найден")

    def do_search_books(self, line):
        search_query = line.lower()
        found_books = []
        for book in self.books:
            if search_query in book.title.lower() or search_query in book.genre.lower() or search_query in book.description.lower():
                if book.available:
                    found_books.append((book.id, book.title))
        if found_books:
            print("Найденные книги:")
            for book_id, book_title in found_books:
                print(f"ID: {book_id}, Название: {book_title}")
        else:
            print("Книги не найдены")

    def do_create_order(self, line):
        user_id, *book_ids = map(int, line.split())
        for book_id in book_ids:
            if not any(book.id == book_id and book.available for book in self.books):
                print(f"Книги с ID {book_id} недоступны")
                return
        order_id = len(self.orders) + 1
        new_order = Order(order_id, user_id, book_ids, Status.CREATED)
        self.orders.append(new_order)
        print(f"Заказ с  ID {new_order.id} был создан")

    def do_complete_order(self, order_id):
        order_id = int(order_id)
        for order in self.orders:
            if order.id == order_id and order.status == Status.CONFIRMED:
                order.status = Status.COMPLETED
                for book_id in order.book_ids:
                    for book in self.books:
                        if book.id == book_id:
                            book.available = True
                print(f"Заказ с ID {order_id} был завершен")
                return
        print(f"Заказ с  ID {order_id} не найден или не подтвержден")


if __name__ == '__main__':
    library_system = LibrarySystem()
    library_system.cmdloop()
```