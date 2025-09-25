import turtle
import math

screen = turtle.Screen
screen.bgcolor("black")
screen.title("Hexagonal Flower illusion")

pen = turtle.turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.pensize(2)

colors = ["cyan", "megenta", "yellow", "white", "lime", "orange"]


def draw_flower_arm(radius, arms):
    for i in range(arms):
        angle = 360 / arms
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(i*angle)
        pen.forward(radius)
        pen.pendown()
        for i in range