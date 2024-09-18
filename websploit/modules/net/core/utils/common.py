import copy
import ctypes
import datetime
import hashlib
import importlib
import math
import multiprocessing
import random
import re
import string
import sys
import time
from websploit.core.utils import CPrint

def replace_dependent_response(log, response_dependent):
    """The `response_dependent` is needed for `eval` below."""

    if str(log):
        key_name = re.findall(re.compile("response_dependent\\['\\S+\\]"), log)
        for i in key_name:
            try:
                key_value = eval(i)
            except Exception:
                key_value = "response dependent error"
            log = log.replace(i, " ".join(key_value))
        return log


def generate_random_token(length=10):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

def now(format="%Y-%m-%d %H:%M:%S"):
    """
    get now date and time
    Args:
        format: the date and time model, default is "%Y-%m-%d %H:%M:%S"

    Returns:
        the date and time of now
    """
    return datetime.datetime.now().strftime(format)

def sort_dictionary(dictionary):
    etc_flag = "..." in dictionary
    if etc_flag:
        del dictionary["..."]
    sorted_dictionary = {}
    for key in sorted(dictionary):
        sorted_dictionary[key] = dictionary[key]
    if etc_flag:
        sorted_dictionary["..."] = {}
    return sorted_dictionary