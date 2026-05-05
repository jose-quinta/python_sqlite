import os
import sqlite3

from app.utils.logger import get_logger

logger = get_logger(__name__)

class Database:
    def __init__(self, db_path: str = 'data/python_sqlite.db') -> None:
        self.db_path = db_path
        self.connection: sqlite3.Connection | None = None
        try:
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                logger.info(f"Created database directory: {db_dir}")

            self.connection = sqlite3.connect(
                db_path,
                timeout=5,
                check_same_thread=False
            )
            logger.info(f"Successfully connected to database: {db_path}")
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database at {db_path}: {str(e)}", exc_info=True)
            raise

    def close_connection(self) -> None:
        if not self.connection:
            logger.warning("No active database connection to close")
            return
        try:
            self.connection.close()
            logger.info("Database connection closed successfully")
        except sqlite3.Error as e:
            logger.error(f"Failed to close database connection: {str(e)}", exc_info=True)
        finally:
            self.connection = None
