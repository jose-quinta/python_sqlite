from typing import Optional, Tuple, List

from lib.orm import Model, CharField, PrimaryKeyField
from lib.utils.logger import get_logger
from app.data.db import get_db
import hashlib
import re

logger = get_logger(__name__)
get_db()

class User(Model):
    _table_name: str = "users"

    id: int = PrimaryKeyField()
    name: str = CharField(max_length=60, null=False)
    firstname: str = CharField(max_length=60, null=False)
    lastname: str = CharField(max_length=60, null=False)
    phonenumber: str = CharField(max_length=8, null=True)
    email: str = CharField(max_length=60, unique=True, null=False)
    password: str = CharField(max_length=64, null=False)

    def __repr__(self) -> str:
        return "<User id={} name={} email={}>".format(self.id, self.name, self.email)

    def _is_hashed(self) -> bool:
        return len(self.password) == 64

    def set_password(self, plain: str) -> None:
        self.password = hashlib.sha256(plain.encode()).hexdigest()

    def verify_password(self, plain: str) -> bool:
        return self.password == hashlib.sha256(plain.encode()).hexdigest()

    def validate(self) -> Tuple[bool, str]:
        if not self.name or len(self.name.strip()) < 2:
            return False, "Name must be at least 2 characters"
        if not self.firstname or len(self.firstname.strip()) < 2:
            return False, "First name must be at least 2 characters"
        if not self.lastname or len(self.lastname.strip()) < 2:
            return False, "Last name must be at least 2 characters"
        if not self._validate_email(self.email):
            return False, "Invalid email format"
        if not self._validate_phone(self.phonenumber):
            return False, "Phone number must be 8 digits"
        if not self.password or len(self.password) < 4:
            return False, "Password must be at least 4 characters"
        return True, "Valid"

    @staticmethod
    def _validate_email(email: str) -> bool:
        pattern: str = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def _validate_phone(phone: str) -> bool:
        if not phone:
            return True
        cleaned: str = re.sub(r'[-\s]', '', phone)
        return cleaned.isdigit() and len(cleaned) == 8

    def to_tuple(self) -> Tuple[Optional[int], str, str, str, str, str, str]:
        return (self.id, self.name, self.firstname, self.lastname,
                self.phonenumber, self.email, self.password)

    @classmethod
    def from_tuple(cls, data: Tuple[Optional[int], str, str, str, str, str, str]) -> 'User':
        user: 'User' = cls()
        user.id = data[0]
        user.name = data[1]
        user.firstname = data[2]
        user.lastname = data[3]
        user.phonenumber = data[4]
        user.email = data[5]
        user.password = data[6]
        return user
