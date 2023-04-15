"""
Log files are create at the root of the project.

TODO: A better way to implement logging it to configure them in a logging service such as DataDog.
"""

import logging
import functools
import os

from datetime import datetime

from src.exceptions import DoesNotExistError, ValidationError, DuplicateRepoName
from github.GithubException import UnknownObjectException, BadCredentialsException


def _generate_log(path):
    """
    Creates a logging object and returns it
    :return:
    """

    logger = logging.getLogger('texas')
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(path)

    # fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    fmt = '%(levelname)s %(asctime)s %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger


def log(path=f"{os.path.abspath(os.curdir)}/logs.error.log"):
    """
    We create a parent function to take arguments
    :param path:
    :return:
    """
    path = f"{os.path.abspath(os.curdir)}/hj.{datetime.date(datetime.now())}.error.log"

    def error_log(func):
        """
        This is the real decorator
        :param func:
        :return:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            logger = _generate_log(path)

            try:
                return func(*args, **kwargs)
            except (DoesNotExistError, ValidationError, DuplicateRepoName) as e:
                err = ' /' + func.__name__
                logger.exception(err)

                return {"message": e.description}, e.code
            except (UnknownObjectException, BadCredentialsException) as e:
                err = ' /' + func.__name__
                logger.exception(err)

                return {"message": e.data.get("message", "An error has occurred")}, e.status
            except Exception as e:
                err = ' /' + func.__name__
                logger.exception(err)

                return {"message": "An error has occurred"}, 500

        return wrapper

    return error_log
