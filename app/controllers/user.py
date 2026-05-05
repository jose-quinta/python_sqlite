import sqlite3
from typing import Any

from app.data.db import Database
from app.entities.user import User
from app.utils.logger import get_logger

logger = get_logger(__name__)

class UserDB(Database):
    def __init__(self, db_path: str = 'data/python_sqlite.db') -> None:
        super().__init__(db_path)
        self.cursor: sqlite3.Cursor | None = self.connection.cursor()
        logger.info("UserDB initialized with database cursor")

    def create_table(self) -> bool:
        try:
            sql_query = '''CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                phonenumber TEXT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );'''
            self.cursor.execute(sql_query)
            self.connection.commit()
            logger.info("User table verified/created successfully")
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to create user table: {str(e)}", exc_info=True)
            return False

    def select_last_id(self) -> int | None:
        sql = 'SELECT id FROM user ORDER BY id DESC LIMIT 1;'
        try:
            self.cursor.execute(sql)
            result: Any = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch last user ID: {str(e)}", exc_info=True)
            return None

    def insert_user(self, user: User) -> tuple[bool, str]:
        is_valid, message = user.validate()
        if not is_valid:
            logger.warning(f"Validation failed for user {user.email}: {message}")
            return False, message

        try:
            query = '''INSERT INTO user(name, firstname, lastname, phonenumber, email, password)
                       VALUES (?, ?, ?, ?, ?, ?)'''
            self.cursor.execute(query, user.to_tuple()[1:])
            self.connection.commit()
            logger.info(f"User {user.email} inserted successfully")
            return True, "User registered successfully"
        except sqlite3.Error as e:
            logger.error(f"Failed to insert user {user.email}: {str(e)}", exc_info=True)
            return False, str(e)

    def select_users(self) -> list[User]:
        try:
            query = '''SELECT id, name, firstname, lastname, phonenumber, email, password
                       FROM user;'''
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [User.from_tuple(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch all users: {str(e)}", exc_info=True)
            return []

    def select_user(self, id: int) -> User | None:
        try:
            query = '''SELECT id, name, firstname, lastname, phonenumber, email, password
                       FROM user WHERE id=?;'''
            self.cursor.execute(query, (id,))
            row = self.cursor.fetchone()
            if row:
                return User.from_tuple(row)
            logger.warning(f"No user found with ID: {id}")
            return None
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch user with ID {id}: {str(e)}", exc_info=True)
            return None

    def update_user(self, id: int, user: User) -> tuple[bool, str]:
        is_valid, message = user.validate()
        if not is_valid:
            logger.warning(f"Validation failed for user update {user.email}: {message}")
            return False, message

        try:
            query = '''UPDATE user
                       SET name=?, firstname=?, lastname=?, phonenumber=?, email=?, password=?
                       WHERE id=?;'''
            self.cursor.execute(query, (
                user.name, user.firstname, user.lastname,
                user.phonenumber, user.email, user.password, id
            ))
            self.connection.commit()
            logger.info(f"User with ID {id} updated successfully")
            return True, "User updated successfully"
        except sqlite3.Error as e:
            logger.error(f"Failed to update user with ID {id}: {str(e)}", exc_info=True)
            return False, str(e)

    def delete_user(self, id: int) -> tuple[bool, str]:
        try:
            query = 'DELETE FROM user WHERE id=?;'
            self.cursor.execute(query, (id,))
            self.connection.commit()
            logger.info(f"User with ID {id} deleted successfully")
            return True, "User deleted successfully"
        except sqlite3.Error as e:
            logger.error(f"Failed to delete user with ID {id}: {str(e)}", exc_info=True)
            return False, str(e)
