class UnsatisfiedResourceException(Exception):

    def __init__(self, message):
        super(UnsatisfiedResourceException, self).__init__(message)
