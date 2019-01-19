

t = None  # will hold Turtle after setup

def setup(turtle_class, this):
    global t
    t = turtle_class(this)

def fd(distance):
    t.forward(distance)
    
def rt(angle):
    t.right(angle)

    
