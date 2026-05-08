import sys
from pathlib import Path
from lib.orm.db import SQLiteAdapter
from lib.orm.config import configure
from lib.utils.logger import get_logger

logger = get_logger(__name__)

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

_db_adapter = None

def init_db():
    global _db_adapter
    if _db_adapter is None:
        _db_adapter = SQLiteAdapter(
            db_directory="data",
            db_name="python_sqlite",
            db_name_extension="db"
        )
        _db_adapter.connect()
        configure(_db_adapter)
        logger.info("Database configured with ORM")
    return _db_adapter

def get_db():
    init_db()
    return _db_adapter

def close_db():
    global _db_adapter
    if _db_adapter:
        _db_adapter.close()
        _db_adapter = None
        logger.info("Database connection closed")
