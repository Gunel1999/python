def show_menu():
    print("\nВыберите необходимое действие:\n"
          "1. Отобразить весь список\n"
          "2. Найти абонента по фамилии\n"
          "3. Изменить номер телефона по фамилии\n"
          "4. Удалить абонента по фамилии\n"
          "5. Найти абонента по номеру телефона\n"
          "6. Добавить нового абонента\n"
          "7. Копировать запись из одного файла в другой\n"
          "8. Завершить работу")
    try:
        choice = int(input("Введите номер действия: "))
    except ValueError:
        print("Ошибка: введите число от 1 до 8.")
        return show_menu()
    return choice


def read_txt(filename):
    phone_book = []
    try:
        with open(filename, 'r', encoding='utf-8') as phb:
            for line in phb:
                line = line.strip()
                if line:
                    fields = line.split(',')
                    if len(fields) == 4:
                        record = {
                            'Фамилия': fields[0].strip(),
                            'Имя': fields[1].strip(),
                            'Телефон': fields[2].strip(),
                            'Описание': fields[3].strip()
                        }
                        phone_book.append(record)
                    else:
                        print(f"Ошибка: строка '{line}' не соответствует ожидаемому формату данных, пропускаю запись.")
                else:
                    print("Пустая строка обнаружена в файле, пропускаю запись.")
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
    return phone_book


def write_txt(filename, phone_book):
    with open(filename, 'w', encoding='utf-8') as phout:
        for person in phone_book:
            phout.write(f"{person['Фамилия']},{person['Имя']},{person['Телефон']},{person['Описание']}\n")


def print_result(phone_book):
    for person in phone_book:
        print(f"{person['Фамилия']}, {person['Имя']}, {person['Телефон']}, {person['Описание']}")


def find_by_lastname(phone_book, last_name):
    found = []
    for person in phone_book:
        if person['Фамилия'].lower() == last_name.lower():
            found.append(person)
    return found if found else "Абонент не найден."


def change_number(phone_book, last_name, new_number):
    found = False
    for person in phone_book:
        if person['Фамилия'].lower() == last_name.lower():
            person['Телефон'] = new_number
            found = True
    
    if found:
        write_txt('phon.txt', phone_book)  # Сохраняем изменения в файл
        return "Номер успешно изменен."
    else:
        return "Абонент с указанной фамилией не найден."


def delete_by_lastname(phone_book, last_name):
    to_delete = []
    for person in phone_book:
        if person['Фамилия'].lower() == last_name.lower():
            to_delete.append(person)
    
    for person in to_delete:
        phone_book.remove(person)
    
    if to_delete:
        write_txt('phon.txt', phone_book)
        return "Абонент успешно удален."
    else:
        return "Абонент не найден."


def find_by_number(phone_book, number):
    found = []
    for person in phone_book:
        if person['Телефон'].strip() == number.strip():
            found.append(person)
    return found if found else "Абонент не найден."


def add_user(phone_book, user_data):
    fields = user_data.strip().split(',')
    if len(fields) != 4:
        return "Ошибка: данные абонента должны содержать Фамилию, Имя, Телефон и Описание, разделенные запятой."
    new_person = {
        'Фамилия': fields[0].strip(),
        'Имя': fields[1].strip(),
        'Телефон': fields[2].strip(),
        'Описание': fields[3].strip()
    }
    phone_book.append(new_person)
    return "Абонент успешно добавлен."


def copy_record(source_phone_book, destination_filename, index):
    try:
        index = int(index) - 1
        if 0 <= index < len(source_phone_book):
            record_to_copy = source_phone_book[index]
            destination_phone_book = read_txt(destination_filename)
            destination_phone_book.append(record_to_copy)
            write_txt(destination_filename, destination_phone_book)
            return f"Запись успешно скопирована в файл '{destination_filename}'."
        else:
            return "Ошибка: указанный номер строки находится вне диапазона доступных записей."
    except ValueError:
        return "Ошибка: номер строки должен быть целым числом."


def work_with_phonebook():
    choice = show_menu()
    phone_book = read_txt('phon.txt')

    while choice != 8:
        if choice == 1:
            print_result(phone_book)
        elif choice == 2:
            last_name = input('Введите фамилию: ')
            print(find_by_lastname(phone_book, last_name))
        elif choice == 3:
            last_name = input('Введите фамилию: ')
            new_number = input('Введите новый номер: ')
            print(change_number(phone_book, last_name, new_number))
        elif choice == 4:
            last_name = input('Введите фамилию: ')
            print(delete_by_lastname(phone_book, last_name))
        elif choice == 5:
            number = input('Введите номер телефона: ')
            print(find_by_number(phone_book, number))
        elif choice == 6:
            user_data = input('Введите данные нового абонента (Фамилия, Имя, Телефон, Описание): ')
            print(add_user(phone_book, user_data))
            write_txt('phon.txt', phone_book)
        elif choice == 7:
            phone_book = input("Введите имя файла, из которого нужно скопировать запись: ")
            destination_filename = input("Введите имя файла, в который нужно скопировать запись: ")
            index = input("Введите номер строки для копирования: ")
            result = copy_record(phone_book, destination_filename, index)
            print(result)

        choice = show_menu()

    print("Работа с телефонной книгой завершена.")


work_with_phonebook()
