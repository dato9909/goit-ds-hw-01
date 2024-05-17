from classes import AddressBook, Record
import pickle



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        
        except IndexError:
            return "Please, enter the name."
        
        except KeyError:
            return "Enter the argument for the command"

    return inner


@input_error
def add_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)
    if record is None:
        record = Record(name)
        contacts.add_record(record)
    record.add_phone(phone)
  
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, old_number, new_number = args
    record = contacts.find(name)
    if record is None:
        raise ValueError("This contact is not exist")
    record.edit_phone(old_number, new_number)
    
    return "Contact updated successfully"

@input_error
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    result = ""
    for ph in record.phones:
        result += str(ph) + " "
    return result

def show_all(contacts):
    return contacts


def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    return record.birthday

def birthdays(contacts):
    return contacts.get_upcoming_birthdays()

def add_birthday(args, contacts):
    name, birthday = args
    record = contacts.find(name)
    if record is None:
        record = Record(name)
        contacts.add_record(record)
    record.add_birthday(birthday)
    return "Birthday is added"


def loadfile():
    try:
        with open("adressbook.pkl", "rb") as file:
            return pickle.load(file)
    except:
        return AddressBook()

def savefile(contacts):
    with open("adressbook.pkl", "wb") as file:
        pickle.dump(contacts, file)


@input_error

def main():

    contacts  = loadfile()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            savefile()
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))
        
        elif command == "change":
            print(change_contact(args,contacts))

        elif command == "phone":
            print(show_phone(args,contacts))
        
        elif command == "all":
            print(show_all(contacts))
        
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        
        elif command == "birthdays":
            print(birthdays(contacts))

    

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
