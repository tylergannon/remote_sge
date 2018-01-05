"A fake DRMAA module to be used as a noop replacement when drmaa is not available."

WARNING = """
    **********************************************************
    The fact that this module is being loaded means that DRMAA
    has not been configured on this system.  This means that
    the application will not actually interact with GridEngine
    through DRMAA.

    Which should only be the case during unit testing, etc.

    Just FYI...
    **********************************************************
"""

print(WARNING)

class InvalidJobException(Exception):
    pass

class Session(object):
    @staticmethod
    def control(_, __):
        pass

    @staticmethod
    def exit():
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False
    
    def __init__(self, _=None):
        pass

    @staticmethod
    def jobStatus(_):
        return u'done'

    def open(self):
        pass

    @staticmethod
    def initialize(_=None):
        pass
