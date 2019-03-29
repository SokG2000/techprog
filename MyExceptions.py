class MyError(Exception):
    pass


class UpgradeError(MyError):
    def __init__(self, text=None):
        if text is not None:
            UpgradeError.txt = text
            MyError.txt = text


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


