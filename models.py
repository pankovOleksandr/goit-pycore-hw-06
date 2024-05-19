"""Module that contains classes for working with address book."""

import re

from collections import UserDict

class Field:
    def __init__(self, value: any):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Field):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    pattern = r"[+\d]"
    country_code = "38"

    def __init__(self, phone_number: str):
        phone_number = "".join(re.findall(self.pattern, phone_number))

        if not phone_number.startswith("+"):
            phone_number = re.sub(fr"^({self.country_code})?", f"+{self.country_code}", phone_number)

        if len(phone_number) != 13:
            raise ValueError(f"Invalid phone number: {phone_number}")

        super().__init__(phone_number)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        if self.find_phone(phone):
            raise ValueError("Phone already exists.")

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, phone: str, new_phone: str):
        phone_to_update = self.find_phone(phone)
        if not phone_to_update:
            raise ValueError("Phone does not exist")

        self.phones[self.phones.index(phone_to_update)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        phone = Phone(phone)
        for p in self.phones:
            if p == phone:
                return p

        return None

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if record.name in self.data:
            raise ValueError(f"Contact {record.name} already exists.")

        self.data[record.name] = record

    def find(self, name: str):
        name = Name(name)

        if name not in self.data:
            raise ValueError("AddressBook does not contain this contact.: {name}")

        return self.data[name]

    def delete(self, name: str):
        name = Name(name)

        if name in self.data:
            del self.data[name]