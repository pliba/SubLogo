from __future__ import print_function
import sys

tortoise_module = sys.modules[__name__]

t = None  # will hold default Tortoise


def forward(distance):
    t.forward(distance)
    
fd = forward

def right(distance):
    t.right(distance)
    
rt = right

def left(distance):
    t.left(distance)
    
lt = left

def goto(x, y):
    t.go_to_point(x, y)
    

def back(distance):
    t.back(distance)


def heading(angle):
    t.heading = angle

class Tortoise(object):
    
    @staticmethod
    def configure(turtle_class, context):
        global t
        t = Tortoise(turtle_class, context)
        #print(dir(turtle_class))
        tortoise_module.__dict__['fd'] = forward
    
    def __init__(self, turtle_class, context):
        it = self.inner_turtle = turtle_class(this)
        
    def forward(self, distance):
        self.inner_turtle.forward(distance)
        
    def right(self, angle):
        self.inner_turtle.right(angle)

    def left(self, angle):
        self.inner_turtle.left(angle)

    def back(self, distance):
        self.inner_turtle.back(distance)

    def go_to_point(self, x, y):
        self.inner_turtle.goToPoint(x, y)
        
    @property
    def heading(self):
        return self.inner_turtle.getHeading()
        
    @heading.setter
    def heading(self, angle):
        self.inner_turtle.setHeading(angle)

        
