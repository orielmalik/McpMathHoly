import logging
import os
from datetime import datetime

#Logger: doesn't print the error to parents log file.
class LoggerSingleton:
    _instance = None

    def __new__(cls, log_dir="logs", log_file=None):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)

            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if log_file is None:
                log_file = f"automation_{timestamp}.log"

            cls._instance.logger = logging.getLogger("AutomationLogger")
            cls._instance.logger.setLevel(logging.DEBUG)

            file_path = os.path.join(log_dir, log_file)
            file_handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler() #StreamHandler ,FileHandler,RotatingFileHandler,HTTPHandler,SocketHandler
            console_handler.setLevel(logging.ERROR)

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(console_handler)
            cls._instance.logger.propagate = False

        return cls._instance

    def get_logger(self):
        return self.logger


logger_instance = LoggerSingleton().get_logger()


def printer(type, value, **kwargs):
    type = type.lower()
    if type == "debug":
        logger_instance.debug(value, **kwargs)
    elif type == "info":
        logger_instance.info(value, **kwargs)
    elif type == "warning":
        logger_instance.warning(value, **kwargs)
    elif type == "error":
        logger_instance.error(value, **kwargs)
    elif type == "critical":
        logger_instance.critical(value, **kwargs)
    else:
        logger_instance.info(f"UNSPECIFIED TYPE: {value}", **kwargs)
