import logging
import sys

def setup_logger(name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configura y retorna un logger centralizado.

    Args:
        name: Nombre del logger. Si es None, usa el root logger.
        level: Nivel de logging (default: INFO)

    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger existente o crea uno nuevo con la configuración por defecto.

    Args:
        name: Nombre del logger (generalmente __name__)

    Returns:
        logging.Logger: Logger configurado
    """
    return setup_logger(name)
