from collections import UserDict
from datetime import datetime, timedelta



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Неправильный телефон")


class Birthday(Field):

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")

            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def edit_phone(self, old_number, new_number):
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                return True

        raise ValueError("Неправильный телефон")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, Birthday: {str(self.birthday)}"


class AddressBook(UserDict):

    def __str__(self) -> str:
        result = ""
        for r in self.values():
            result += str(r) + "\n"
        return result

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find_next_weekday(self, d, weekday=0):
        # Функция для нахождения следующего заданного дня недели после заданной даты
        # d : datatime.date - начальная дата
        # weekday : int - день недели от 0 до 6

        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Если день рождения уже прошел
            days_ahead += 7
        return d + timedelta(days=days_ahead)

    def replace_prepared_users(self):

        prepared_users = []

        for user in self.values():
            try:
                birthday = user.birthday.value.date()
                prepared_users.append({"name": user.name.value, "birthday": birthday})
            except ValueError:
                print(f"Неккоректна дата народження для користувача {user.name.value}")
        return prepared_users

    def get_upcoming_birthdays(self, days=7):

        today = datetime.today().date()

        upcoming_birthdays = []

        prepared_users = self.replace_prepared_users()

        for user in prepared_users:
            birthday_this_year = user["birthday"].replace(
                year=today.year
            )  # 1985 -> 2024

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                if birthday_this_year.weekday() >= 5:  # Суббота, воскресенье
                    birthday_this_year = self.find_next_weekday(
                        birthday_this_year, 0
                    )  # понедельник

                congratulation_date_str = birthday_this_year.strftime("%Y.%m.%d")
                upcoming_birthdays.append(
                    {
                        "name": user["name"],
                        "congratulation_date": congratulation_date_str,
                    }
                )

        return upcoming_birthdays


def main():
    # Создаем новую адресную книгу
    book = AddressBook()

    # Создаем записи для контактов
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")

    # Добавляем записи в адресную книгу
    book.add_record(john_record)
    book.add_record(jane_record)

    # Выводим все записи в книге
    for name, record in book.data.items():
        print(record)

    # Изменяем номер телефона у записи John
    book.edit_phone(john_record, "1234567890", "1112223333")

    # Поиск записи John
    found_record = book.find_record("John")
    if found_record:
        print("Найдена запись John:", found_record)
    else:
        print("Запись John не найдена.")

    # Удаляем запись Jane
    book.delete_record("Jane")


if __name__ == "__main__":
    main()


"""
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

"""
