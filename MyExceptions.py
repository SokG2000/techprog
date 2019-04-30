import functools


class MyError(Exception):
    pass


class UpgradeError(MyError):
    def __init__(self, text=None):
        if text is not None:
            UpgradeError.txt = text
            MyError.txt = text


class FunctionBreakError(MyError):
    pass


def catch_break_error(func):
    @functools.wraps(func)    
    def wraps(*args, **qwargs):
        try:
            return func(*args, **qwargs)
        except FunctionBreakError:
            pass
    return wraps

class EndGameException(MyError):
    pass

class BuildError(MyError):
    def __init__(self, text=None):
        if text is not None:
            BuildError.txt = text
            MyError.txt = text


class HireError(MyError):
    def __init__(self, text=None):
        if text is not None:
            HireError.txt = text
            MyError.txt = text


