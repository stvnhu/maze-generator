
from tkinter import Tk, Canvas

class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Generator")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack()
    
    def mainloop(self):
        self.__root.mainloop()

    def draw_line(self, line: Line):
        line.draw(self.__canvas)

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p0: Point, p1: Point):
        self.p0 = p0
        self.p1 = p1
    
    def draw(self, canvas: Canvas):
        canvas.create_line(self.p0.x, self.p0.y, self.p1.x, self.p1.y, width=2)