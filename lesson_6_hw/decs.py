from functools import wraps
from lesson_5_hw.log import server_log_config
from lesson_5_hw.log import client_log_config
import inspect
from datetime import datetime

server_logger = server_log_config.logger
client_logger = client_log_config.logger


def log(func):
    @wraps(func)
    def call(*args, **kwargs):
        outer_func = inspect.stack()[1][3]
        server_logger.debug(f'Function {func.__name__} is called into {outer_func} at {datetime.now()}')
        client_logger.debug(f'Function {func.__name__} is called into {outer_func} at {datetime.now()}')
        return func(*args, **kwargs)

    return call
