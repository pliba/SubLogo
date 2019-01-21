from __future__ import print_function

from parser import tokenize, parse_exp
from evaluator import evaluate, define_function, Operator, VALUE_OPS
import errors
import turtle
add_library('Turtle')

TESTING = True

def setup():
    size(500,500)
    background(255)
    stroke(0)
    turtle.setup(Turtle, this)
    print(dir(turtle))
    if not TESTING:
        selectInput("Select a file to process:", "fileSelected")
    else:
        #selected_path = '/home/luciano/sketchbook/SubLogo/gcd.sublogo'
        selected_path = '/home/luciano/sketchbook/SubLogo/square.sublogo'
        with open(selected_path) as source:
            run(source)      

def fileSelected(selection):
    if selection == None:
        print("Window was closed or the user hit cancel.")
    else:
        selected_path = selection.getAbsolutePath()
        print("User selected " + selected_path)
        with open(selected_path) as source:
            run(source)      

TURTLE_OPS = [
    Operator('fd', turtle.fd, 1),
    Operator('rt', turtle.rt, 1),
]

VALUE_OPS.update({op.name: op for op in TURTLE_OPS})

def run(source_file):
    """Read and execute opened source file"""
    source = source_file.read()
    env = {}
    tokens = tokenize(source)

    while tokens:
        try:
            current_exp = parse_exp(tokens)
        except errors.UnexpectedCloseParen as exc:
            print('***', exc, file=sys.stderr)
            break

        if isinstance(current_exp, list) and current_exp[0] == 'define':
            define_function(current_exp[1:])
        else:
            try:
                evaluate(env, current_exp)
            except errors.EvaluatorException as exc:
                print('***', exc, file=sys.stderr)
                continue
