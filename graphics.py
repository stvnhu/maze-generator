
from tkinter import Tk, Canvas, BooleanVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze import Line

class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Generator")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack()
        self.__free_to_draw = BooleanVar(value=False)
    
    def mainloop(self):
        self.__root.mainloop()
    
    def make_line(self, line: Line, width: int = 2, color: str = "black"):
        return self.__canvas.create_line(line.p0.x, line.p0.y, line.p0.x, line.p0.y, width=width, fill=color)

    def draw_line(self, line: Line, remaining_line_count: list, steps: int = 100, animation_delay: int = 1):
        dx = (line.p1.x - line.p0.x) / steps
        dy = (line.p1.y - line.p0.y) / steps

        match line.direction:
            case 1:
                start_x = line.p0.x
                start_y = line.p0.y
            case -1:
                start_x = line.p1.x
                start_y = line.p1.y
                dx = -dx
                dy = -dy
            
        def animate(step=0):
            if step > steps:
                remaining_line_count[0] -= 1
                line.drawn = True
                if remaining_line_count[0] == 0:
                    self.__free_to_draw.set(True)
                return
            self.__canvas.coords(line.line, start_x, start_y, start_x + dx * step, start_y + dy * step)
            self.__root.after(animation_delay, animate, step + 1)
        
        animate()
    
    def wait_animation(self):
        self.__root.wait_variable(self.__free_to_draw)
        self.__free_to_draw.set(False)