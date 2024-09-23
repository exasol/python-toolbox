# With Decorator
import logging
from functools import wraps


def log_execution(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logging.debug(f"Entering: {f.__name__}")
        result = f(*args, **kwargs)
        logging.debug(f"Leaving: {f.__name__}")
        return result

    return wrapper


@log_execution
def some_function():
    return "Some Result"


@log_execution
def other_function():
    return "Other Result"


# Naive Approach
import logging


def some_function():
    logging.debug("Entering: some_function")
    result = "Some Result"
    logging.debug("Leaving: some_function")
    return result


def other_function():
    logging.debug("Entering: other_function")
    result = "Some Result"
    logging.debug("Leaving: other_function")
    return result
