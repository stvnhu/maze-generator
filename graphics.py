
from tkinter import Tk, Canvas, BooleanVar
from maze import Line

class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Generator")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack()
        self.__drawing = BooleanVar(value=False)
    
    def mainloop(self):
        self.__root.mainloop()
    
    def add_line(self, line: Line, width: int = 2, color: str = "black"):
        return self.__canvas.create_line(line.p0.x, line.p0.y, line.p0.x, line.p0.y, width=width, fill=color)

    def draw_line(self, line: Line, direction: int, remaining_line_count: list, steps: int = 50, animation_delay: int = 10):
        dx = (line.p1.x - line.p0.x) / steps
        dy = (line.p1.y - line.p0.y) / steps

        def animate(step=0):
            if step > steps:
                remaining_line_count[0] -= 1
                if not remaining_line_count[0]:
                    self.__drawing.set(True)
                return
            if direction == 1:
                self.__canvas.coords(line.line, line.p0.x, line.p0.y, line.p0.x + dx * step, line.p0.y + dy * step)
            else:
                self.__canvas.coords(line.line, line.p1.x, line.p1.y, line.p1.x - dx * step, line.p1.y - dy * step)

            self.__root.after(animation_delay, animate, step + 1)
        
        if not line.exists:
            animate(101)
        else:
            animate()
    
    def wait_animation(self):
        
        self.__root.wait_variable(self.__drawing)
        self.__drawing.set(False)