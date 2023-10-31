from functools import wraps


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