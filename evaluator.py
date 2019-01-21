import operator

import errors


VARIADIC = -1  # arity of variadic functions or forms


def check_arity(form_name, arity, args):
    if arity == VARIADIC:
        return
    error_type = None
    if len(args) > arity:
        error_type = errors.TooManyArguments
    elif len(args) < arity:
        error_type = errors.MissingArgument
    if error_type:
        raise error_type('{!r} needs {}'.format(form_name, arity))


class Operator:

    def __init__(self, name, function, arity):
        self.name = name
        self.function = function
        self.arity = arity

    def __call__(self, *args):
        check_arity(self.name, self.arity, args)
        return self.function(*args)


def print_fn(n):
    print(n)
    return n


def line_fn(*args):
    line(*args)

BUILT_INS = [
    Operator('+', operator.add, 2),
    Operator('-', operator.sub, 2),
    Operator('*', operator.mul, 2),
    Operator('/', operator.floordiv, 2),
    Operator('=', operator.eq, 2),
    Operator('<', operator.lt, 2),
    Operator('>', operator.gt, 2),
    Operator('print', print_fn, 1),
    # graphics
    Operator('line', line_fn, 4),
    
]

VALUE_OPS = {op.name: op for op in BUILT_INS}


class SpecialForm:

    @property
    def name(self):
        class_name = self.__class__.__name__
        return class_name.replace('Statement', '').lower()

    def __call__(self, environment, *args):
        check_arity(self.name, self.arity, args)
        return self.apply(environment, *args)


class SetStatement(SpecialForm):
    arity = 2

    def apply(self, environment, name, val_exp):
        value = evaluate(environment, val_exp)
        if name in environment:
            environment[name] = value
        else:
            global_environment[name] = value
        return value


class IfStatement(SpecialForm):
    arity = 3

    def apply(self, environment, condition, consequence, alternative):
        if evaluate(environment, condition):
            return evaluate(environment, consequence)
        else:
            return evaluate(environment, alternative)


class BeginStatement(SpecialForm):
    arity = VARIADIC

    def apply(self, environment, *statements):
        for statement in statements[:-1]:
            evaluate(environment, statement)
        return evaluate(environment, statements[-1])


class WhileStatement(SpecialForm):
    arity = 2

    def apply(self, environment, condition, block):
        while evaluate(environment, condition):
            evaluate(environment, block)
        return 0


class RepeatStatement(SpecialForm):
    arity = -1

    def apply(self, environment, times, *actions):
        n = evaluate(environment, times)
        for i in range(n):
            for action in actions:
                evaluate(environment, action)
        return i


CONTROL_OPS = {
    'set': SetStatement(),
    'if': IfStatement(),
    'begin': BeginStatement(),
    'while': WhileStatement(),
    'repeat': RepeatStatement(),
}


FUNC_TEMPLATE = '<UserFunction ({.name} {})>'

class UserFunction:

    def __init__(self, name, formals, body):
        self.name = name
        self.formals = formals
        self.arity = len(formals)
        self.body = body

    def __repr__(self):
        formals = ' '.join(self.formals)
        return FUNC_TEMPLATE.format(self, formals)

    def __call__(self, *values):
        check_arity(self.name, self.arity, values)
        local_env = dict(zip(self.formals, values))
        return evaluate(local_env, self.body)


def define_function(parts):
    name, formals, body = parts
    user_fn = UserFunction(name, formals, body)
    function_definitions[name] = user_fn
    return repr(user_fn)


global_environment = {}

function_definitions = {}


def fetch_variable(environment, name):
    try:
        return environment[name]
    except KeyError:
        try:
            return global_environment[name]
        except KeyError as exc:
            raise errors.UndefinedVariable(name)


def fetch_function(name):
    try:
        return VALUE_OPS[name]
    except KeyError:
        try:
            return function_definitions[name]
        except KeyError as exc:
            raise errors.UndefinedFunction(name)


def evaluate(environment, expression):
    """Given an environment, evaluate expression."""

    if isinstance(expression, int):  # number
        return expression

    if isinstance(expression, str):  # variable
        return fetch_variable(environment, expression)

    else:  # application expression
        op_name = expression[0]
        args = expression[1:]
        if op_name in CONTROL_OPS:
            op = CONTROL_OPS[op_name]
            return op(environment, *args)
        else:
            op = fetch_function(op_name)
            values = (evaluate(environment, x) for x in args)
            try:
                return op(*values)
            except ZeroDivisionError as exc:
                raise errors.DivisionByZero()
