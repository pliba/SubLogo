from __future__ import division
add_library('Turtle')

from tortoise import *


def setup():
    size(600,600)
    background(255)
    stroke(0)
    Tortoise.configure(Turtle, this)
    noLoop()
    
    
def draw():
    #quad(100)
    #quadespi(3)
    demo_poligonos()
    #demo_poly()
    #demo_arvore()
    #demo_poliespi()
    #demo_seta()
   

def quad(lado):
    for _ in range(4):
        fd(lado)
        rt(90)
    
def quadespi(lado):
    if lado > (width/5):
        return
    quad(lado)
    rt(20)
    quadespi(lado+5)
                
def poligono(lados, lado):
    for _ in range(lados):
        fd(lado)
        rt(360/lados)
            
def demo_poligonos():
    heading(0)
    goto(10, 300)
    for lados in range(3, 31):
        poligono(lados, 50)
    goto(10, 275)
    poligono(360, 4.5)
            
def demo_poly():
    goto(130, 310)
    poly(300, 156)
    goto(250, 450)
    poly(200, 160)
    goto(450, 450)
    poly(120, 80)
    goto(450, 100)
    poly(100, 144)
    goto(480, 180)
    poly(120, 160)
    
def poly(lado, angulo, contagem=0):
    if contagem > 100:
        return
    fd(lado)
    rt(angulo)
    poly(lado, angulo, contagem+1)    

def demo_arvore():
    goto(300, 600)
    arvore(40, 15, 5)        

def arvore(lado, angulo, nivel):
    if nivel == 0:
        return
    lt(angulo)
    fd(2 * lado)
    arvore(lado, angulo, nivel-1)
    back(2 * lado)
    rt(2 * angulo)
    fd(lado)
    arvore(lado, angulo, nivel-1)
    back(lado)
    lt(angulo)
    
    
def demo_poliespi():
    goto(150, 150)
    poliespi(1, 45, 1)
    goto(150, 450)
    poliespi(5, 120, 5)
    goto(450, 450)
    poliespi(5, 144, 5)
    

def poliespi(lado, angulo, incremento):
    if lado > (width/5):
        return
    fd(lado)
    rt(angulo)
    poliespi(lado+incremento, angulo, incremento)

def demo_seta():
    goto(300, 300)
    seta(150)
    
def seta(tam):
    fd(tam)
    rt(150)
    fd(tam/6)
    back(tam/6)
    lt(300)
    fd(tam/6)
