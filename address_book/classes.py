from collections import UserDict
from datetime import datetime, date
from abc import ABC, abstractmethod
import re
from typing import List

class Field(ABC):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    @abstractmethod
    def is_valid(self, value):
        raise NotImplementedError

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        return value.isdigit() and len(value) == 10


class Address(Field):
    def is_valid(self, value):
        return True
    
    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def is_valid(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)


class Email(Field):
    def is_valid(self, value):
        if value:
            return re.fullmatch(r'([a-zA-Z]{1}[a-zA-Z0-9._]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})', value)
        return False
            

class Record:
    def __init__(self, name: Name, phone: List[Phone], birthday: Birthday, email: Email, address: Address):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.phones.append(Phone(phone.value))
        self.birthday = Birthday(birthday).value if birthday != "Not set" else birthday
        self.email = Email(email).value if email != "Not set" else email
        self.address = Address(address).value if address != "Not set" else address
    
    def add_phone(self, phone: Field):
        phone = Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)

    def remove_phone(self, phone: Field):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)

    def change_phone(self, phone:Phone=None, new_phone:Phone=None, phone_obj:Phone=None, new_phone_obj:Phone=None):
        if phone != None and new_phone != None:
            phone = Phone(phone)
            new_phone = Phone(new_phone)
        elif phone_obj != None and new_phone_obj != None:
            phone = phone_obj
            new_phone = new_phone_obj
        
        try:
            index = self.phones.index(phone)
            self.phones[index] = new_phone
        except ValueError:
            return 'Contacts has no such phone'
        
        return "Phone '{phone.value}' was successfuly changed to '{new_phone.value}'"
    
    def change_birthday(self, birthday):
        birthday = Birthday(birthday)
        self.birthday = str(birthday)
    
    def change_email(self, email):
        email = Email(email)
        self.email = str(email)

    def change_address(self, address: Address):
        self.address = Address(address)
       
                
    def find_phone(self, phone: Phone):
        for i in self.phones:
            if i.value == phone.value:
                return i.value
        return None
    
    def days_to_birthday(self, birthday):
        if self.birthday:
            today = date.today()
            next_birthday = datetime.strptime(str(self.birthday), '%d.%m.%Y')
            birthday_day = date(year=today.year, month=next_birthday.month, day=next_birthday.day)

            if today > birthday_day:
                birthday_day = date(year=today.year + 1, month=next_birthday.month, day=next_birthday.day)

            days = birthday_day - today
            return days.days
        return None
    
    def get_phones(self):
        if len(self.phones) > 0:
            return ', '.join([phone.value for phone in self.phones])
        else:
            return 'Contact has no phones'

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}, email: {self.email}, address: {self.address}"
    

class AddressBook(UserDict):

    def add_record(self, record):
        if record.name.value in self.data:
            return self.data[record.name.value]
        self.data[record.name.value] = record
        return record

    def find(self, name):
        for record in self.data.values():
            if name in record.name.value:
                return record
        return f"There is no contacts with name '{name}'"

    def delete(self, record):
        try:
            del self.data[record.name.value]
        except KeyError:
            print('Contact not found')
        
        return 'Contact was successfully deleted!'

    def iterator(self, n=1):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i: i+n]

    def get_records(self):
        records = '|{:^10}|{:^20}|{:^15}|{:^15}|{:^20}\n'.format("Name", "Phones", "Birthday", "Email", "Address")
        for record in self.data.values():
            records += '|{:^10}|{:^20}|{:^15}|{:^15}|{:^20}\n'.format(record.name.value,\
                ', '.join(p.value for p in record.phones), str(record.birthday), str(record.email), str(record.address))
        return records

    def __str__(self) -> str:
        return '\n'.join(str(r) for r in self.data.values())
    