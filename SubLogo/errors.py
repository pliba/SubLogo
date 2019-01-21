class InterpreterException(Exception):
    """Generic interpreter exception."""

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        msg = self.__class__.__doc__
        if self.value is not None:
            msg = msg.rstrip('.')
            if "'" in self.value:
                value = self.value
            else:
                value = repr(self.value)
            msg += ': {}.'.format(value)
        return msg


class ParserException(InterpreterException):
    """Generic exception while parsing."""


class UnexpectedCloseParen(ParserException):
    """Unexpected close parenthesis."""


class UnexpectedEndOfSource(ParserException):
    """Unexpected end of source code."""


class EvaluatorException(InterpreterException):
    """Generic exception while evaluating."""


class UndefinedVariable(EvaluatorException):
    """Undefined variable."""


class UndefinedFunction(EvaluatorException):
    """Undefined function."""


class DivisionByZero(EvaluatorException):
    """Division by zero."""


class TooManyArguments(EvaluatorException):
    """Too many arguments."""


class MissingArgument(EvaluatorException):
    """Missing argument."""
