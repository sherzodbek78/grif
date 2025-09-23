import turtle
a=3
b=1
turtle.speed(15)
turtle.bgcolor('black')
turtle.pencolor('cyan')
turtle.penup()
turtle.goto(0,200)
turtle.pendown()
while True:
    turtle.forward(a)
    turtle.right(b)
    a+=3
    b+=1