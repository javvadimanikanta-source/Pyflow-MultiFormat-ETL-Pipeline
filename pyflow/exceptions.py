class PyFlowError(Exception):
    pass


class ConfigError(PyFlowError):
    pass


class ExtractionError(PyFlowError):
    pass


class ValidationError(PyFlowError):
    pass


class TransformationError(PyFlowError):
    pass


class LoadingError(PyFlowError):
    pass
