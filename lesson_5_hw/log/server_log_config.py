import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("server_log")

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)-4s - %(module)-4s - %(message)s "
)
f_h = TimedRotatingFileHandler(
    "lesson_5_hw/log/server_logs.log", encoding="utf-8", when="D", interval=1
)
f_h.setFormatter(formatter)
f_h.setLevel(logging.DEBUG)

logger.addHandler(f_h)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info("Testing logger")
