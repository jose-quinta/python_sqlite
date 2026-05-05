from dataclasses import dataclass
import hashlib
import re


@dataclass
class User:
    id: int = 0
    name: str = 'anonymous'
    firstname: str = 'firstname'
    lastname: str = 'lastname'
    phonenumber: str = '0000-0000'
    email: str = 'example@gmail.com'
    password: str = '12345'

    def __post_init__(self):
        if self.password and not self._is_hashed(self.password):
            self.password = self.hash_password(self.password)

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def _is_hashed(password: str) -> bool:
        return len(password) == 64

    def verify_password(self, plain_password: str) -> bool:
        return self.password == self.hash_password(plain_password)

    def to_tuple(self) -> tuple[int, str, str, str, str, str, str]:
        return (self.id, self.name, self.firstname, self.lastname,
                self.phonenumber, self.email, self.password)

    @classmethod
    def from_tuple(cls, data: tuple[int, str, str, str, str, str, str]) -> 'User':
        return cls(
            id= data[0],
            name= data[1],
            firstname= data[2],
            lastname= data[3],
            phonenumber= data[4],
            email= data[5],
            password= data[6]
        )

    def validate(self) -> tuple[bool, str]:
        if not self.name or len(self.name.strip()) < 2:
            return False, "Name must be at least 2 characters"

        if not self.firstname or len(self.firstname.strip()) < 2:
            return False, "First name must be at least 2 characters"

        if not self.lastname or len(self.lastname.strip()) < 2:
            return False, "Last name must be at least 2 characters"

        if not self._validate_email(self.email):
            return False, "Invalid email format"

        if not self._validate_phone(self.phonenumber):
            return False, "Phone number must be 10 digits or format 0000-0000"

        if not self.password or len(self.password) < 4:
            return False, "Password must be at least 4 characters"

        return True, "Valid"

    @staticmethod
    def _validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def _validate_phone(phone: str) -> bool:
        cleaned = re.sub(r'[-\s]', '', phone)
        return cleaned.isdigit() and len(cleaned) == 8

    def __str__(self) -> str:
        return f'''\tID: {self.id}
        Name: {self.name} {self.firstname} {self.lastname}
        Phonenumber: {self.phonenumber}
        Email: {self.email}
        Password: {'******' if self._is_hashed(self.password) else self.password}'''
