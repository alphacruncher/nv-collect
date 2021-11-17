class NVCollectException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.msg}"


class NoCollectiblesException(NVCollectException):
    def __init__(self, msg):
        super().__init__(msg)


class WrongAssignmentFolderException(NVCollectException):
    def __init__(self, msg):
        super().__init__(msg)


class WrongAssignmentNameException(NVCollectException):
    def __init__(self, msg):
        super().__init__(msg)


class AmbiguousCopySourceException(NVCollectException):
    def __init__(self, msg):
        super().__init__(msg)


class ManifestMissingException(NVCollectException):
    def __init__(self, msg):
        super().__init__(msg)


class SourceDoesNotExistException(NVCollectException):
    def __init__(self, msg):
        super().__init__(msg)
