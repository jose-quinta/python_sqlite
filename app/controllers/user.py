from typing import Optional, List
from lib.utils.logger import get_logger
from app.entities.user import User

logger = get_logger(__name__)

class UserDB:
    def __init__(self):
        pass

    def select_users(self) -> List[User]:
        try:
            users = User.objects.all()
            logger.info("Fetched {} users".format(len(users)))
            return users
        except Exception as e:
            logger.error("Failed to fetch users: {}".format(e), exc_info=True)
            return []

    def select_user(self, user_id: int) -> Optional[User]:
        try:
            user = User.objects.get(id=user_id)
            return user
        except Exception as e:
            logger.warning("User with ID {} not found: {}".format(user_id, e))
            return None

    def insert_user(self, user: User) -> tuple:
        try:
            is_valid, message = user.validate()
            if not is_valid:
                return False, message
            
            user.save()
            logger.info("User {} inserted successfully".format(user.email))
            return True, "User registered successfully"
        except Exception as e:
            logger.error("Failed to insert user: {}".format(e), exc_info=True)
            return False, str(e)

    def update_user(self, user_id: int, updated_user: User) -> tuple:
        try:
            is_valid, message = updated_user.validate()
            if not is_valid:
                return False, message
            
            user = User.objects.get(id=user_id)
            user.name = updated_user.name
            user.firstname = updated_user.firstname
            user.lastname = updated_user.lastname
            user.phonenumber = updated_user.phonenumber
            user.email = updated_user.email
            user.password = updated_user.password
            user.save()
            
            logger.info("User with ID {} updated successfully".format(user_id))
            return True, "User updated successfully"
        except Exception as e:
            logger.error("Failed to update user {}: {}".format(user_id, e), exc_info=True)
            return False, str(e)

    def delete_user(self, user_id: int) -> tuple:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            logger.info("User with ID {} deleted successfully".format(user_id))
            return True, "User deleted successfully"
        except Exception as e:
            logger.error("Failed to delete user {}: {}".format(user_id, e), exc_info=True)
            return False, str(e)

    def count_users(self) -> int:
        try:
            return User.objects.count()
        except Exception as e:
            logger.error("Failed to count users: {}".format(e), exc_info=True)
            return 0
    
    def close(self) -> None:
        pass
