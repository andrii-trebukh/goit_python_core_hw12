import re
from addressbook import Record, AddressBook

book = AddressBook()

commands = {}

exit_flag = False


def command_handler(command):
    def input_error(func):
        def wrapper(*args):
            try:
                return func(*args)
            except TypeError as err:
                return f"Incorrect input: {err}\n{help_command()}"
            except ValueError as err:
                return err

        commands_list = (command, ) if isinstance(command, str) else command
        for i in commands_list:
            commands[i] = wrapper

        return wrapper
    return input_error


@command_handler("help")
def help_command(*args):
    return "Usage: command [name] [phone number] [birthday]\n"\
        "list - list all commands"


@command_handler("list")
def list_command(*args):
    return "\n".join(commands)


@command_handler(("show all", "show"))
def show_all_command(*args):
    if not book.data:
        raise ValueError("It's empty. There are no any records.")
    output = [str(record) for record in book.data.values()]
    return "\n".join(output)


@command_handler(("good bye", "close", "exit", "."))
def exit_command(*args):
    global exit_flag
    exit_flag = True
    book.save_csv("addressbook.csv", overwrite=True)
    return "Good bye!"


@command_handler("hello")
def hello_command(*args):
    return "How can I help you?"


@command_handler("add")
def add_command(name, phone=None, birthday=None):
    record = Record(name, birthday)
    if phone:
        record.add_phone(phone)
    book.add_record(record)
    return f"New name {name} has been added"


@command_handler("phone add")
def add_phone_command(name, phone):
    record = book.find(name)
    record.add_phone(phone)
    return f"Phone number {phone} for name {name} has been added"


@command_handler("phone remove")
def remove_phone_command(name, phone):
    record = book.find(name)
    record.remove_phone(phone)
    return f"Phone number {phone} for name {name} has been removed"


@command_handler("phone edit")
def edit_phone_command(name, old_phone, new_phone):
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return f"Phone number {old_phone} for name {name} "\
        f"has been changed to {new_phone}"


@command_handler("remove")
def remove_command(name):
    book.delete(name)
    return f"{name} phone number has been removed"


@command_handler("phone")
def phone_command(name):
    record = book.find(name)
    return str(record)


@command_handler("birthday")
def set_birthday_command(name, birthday):
    record = book.find(name)
    record.set_birthday(birthday)
    return f"Birthday has been set to {birthday}"


@command_handler("find")
def find_command(sample):
    output = [str(record) for record in book.find_sample(sample)]
    if not output:
        return "Nothing found"
    return "Contacts found:\n" + "\n".join(output)


def main():

    book.load_csv("addressbook.csv")

    while not exit_flag:
        input_string = input(">>> ")
        input_string = input_string.strip()

        # some workaround: adding space at the end of the string
        # need for correct detection of the command without args
        # will be further stripped
        input_string += " "

        command = None
        for check_command in commands:

            if input_string.lower().startswith(f"{check_command} "):
                command = check_command
                args = input_string[len(check_command):]

                # removing excess spaces
                args = args.strip()
                args = re.sub(r"\s+", " ", args)

                args = args.split(" ")
                break

        if command is None:
            print("No such command")
            continue

        print(commands[command](*args))


if __name__ == "__main__":
    main()
