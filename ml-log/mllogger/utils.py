from functools import wraps
import time
import random

def single(cls):
    _instance = {}
    @wraps(cls)
    def _single(*args,**kwargs):
        # nonlocal _instance
        if cls not in _instance :
            _instance[cls] = cls(*args,**kwargs) 
        else:
            pass
        return _instance[cls]
    return _single
def format_time() ->str:
    return time.strftime("%Y%m%d%H%M%S", time.localtime())
def has_multiple_keys(dictionary:dict, *keys)->bool:
    return set(keys).issubset(dictionary.keys())
def new_experiment_id() -> str:
        digits = [str(random.randint(0, 9)) for _ in range(15)]
        id = "".join(digits)
        return id