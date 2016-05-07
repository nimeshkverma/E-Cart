class ErrorMessage(Exception):

    def __init__(self, msg):
        self.value = msg

    def __str__(self):
        return repr(self.value)
