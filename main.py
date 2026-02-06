
from graphics import Window
from maze import Maze

def main():
    
    # must be bigger than 1x1
    COLUMNS = 15
    ROWS = 15
    CELL_SIZE = 50
    MARGIN = 50

    width = 2 * MARGIN + COLUMNS * CELL_SIZE
    height = 2 * MARGIN + ROWS * CELL_SIZE

    window = Window(width , height)

    maze = Maze(window, COLUMNS, ROWS, CELL_SIZE, MARGIN)
    maze.generate_maze()
    maze.draw()

    window.mainloop()

if __name__ == "__main__":
    main()