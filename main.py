
from graphics import *

class Cell:
    def __init__(self, window: Window, p0: Point, size: int):
        self.window = window
        self.p0 = p0
        self.p1 = Point(p0.x + size, p0.y)
        self.p2 = Point(p0.x + size, p0.y + size)
        self.p3 = Point(p0.x, p0.y + size)
    
    def draw(self):
        line = Line(self.p0, self.p1)
        self.window.draw_line(line)
        line = Line(self.p1, self.p2)
        self.window.draw_line(line)
        line = Line(self.p2, self.p3)
        self.window.draw_line(line)
        line = Line(self.p3, self.p0)
        self.window.draw_line(line)

def main():
    
    window = Window(800, 600)

    cell = Cell(window, Point(50, 50), 50)
    cell.draw()

    window.mainloop()

if __name__ == "__main__":
    main()