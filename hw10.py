from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    pass
        
class Record:
    def __init__(self, name: Name, phone: Phone=None):
        self.name = name
        self.phones = [phone] if phone else []

    def add_phone(self, phone):
        self.phones.append(phone)
        
    def change_phone(self, index, phone):
        self.phones[index] = phone
        
    def delete_phone(self, phone):
        self.phones.remove(phone)
    
class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        self.data[name] = record
    

phone_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return 'Contact with that name not found.'
        except ValueError:
            return 'Please enter a valid command.'
        except IndexError:
            return 'Please enter both name and phone number, separated by a space.'
    return wrapper

def decorator_main(func):
    def wrap(*word):
        print('----Phone book Console Bot----\n'
              ' Commands: \n'
              '     hello - start bot\n'
              '     add - add new contact \n'
              '     change - change contact phone \n'
              '     phone - Search by name \n'
              '     show all - Show all list contact\n'
              '     goodbye, close, . - exit')
        print('-'*30)
        print(func())
    return wrap

def hello():
    return 'How can I help you?'

def good_bye():
    return 'Good bye!'


@input_error
def add_c():
    n_p = input('Enter name and phone:').split(' ')

    name = Name(str(n_p[0]).title())
    phone = Phone(n_p[1:])
    record = Record(name,phone)
    phone_book.add_record(record)

    return f'{name.value} : {phone.value} Add successful!'

    
@input_error
def change():
    n_p = input('Enter Name and phone:').split(' ')
    
    name = Name(n_p[0])
    phone = Phone( n_p[1:])
    record = phone_book[name.value]
    record.change_phone(0, phone)
    
    return f'{name.value} : {phone.value} Change successful!'

@input_error
def phones() -> str:
    src_by_name = input('Enter name:')
    
    if src_by_name in phone_book.data:
        for key, val in phone_book.data.items():
            record = phone_book.data[key]
            if src_by_name == key:
                return f"Phone: {', '.join(str(phone) for phone in record.phones)}"
            
    return 'Not find!'       
        
def decor_table(func):
    def wrapper(*words):
        print(' -'*19)
        print("|{:^5}|{:^15}|{:^15}".format('#', 'Name', 'Phone'))
        print(' -'*19)
        func(*words)
        print(' -'*19)
    return wrapper
 
@decor_table        
def show_all():
    if len(phone_book.data) == 0:  
        print("No contacts found")
    else:
        i = 1
        for k,v in phone_book.data.items():    
            record = phone_book.data[k]  
            print("{:^5} {:^15}   {}".format(i, k, ', '.join(str(phone) for phone in record.phones)))
            i += 1
            

COMMAND_DICT = {'hello': hello,
                 'add': add_c,
                 'change': change,
                 'phone': phones,
                 'show all': show_all,
                 'goodbye': good_bye,
                 'close': good_bye,
                 '.': good_bye}


def get_command(words):
    if words in COMMAND_DICT:
        return COMMAND_DICT[words]
    raise KeyError("This command doesn't exist")

@decorator_main
def main():
    while True:
        input_c = input(">>> ")
        
        func = get_command(input_c)
        print(func())
        
        if input_c in ['goodbye', 'close', '.']:
            break
        
if __name__ == '__main__':
    main()