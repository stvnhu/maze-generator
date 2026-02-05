
import random
from graphics import Window

class Maze:
    def __init__(self, window: Window, columns: int, rows: int, cell_size: int, margin: int):
        self.__window = window
        self.__columns = columns
        self.__rows = rows
        self.__cell_size = cell_size
        self.__margin = margin
        
        self.__draw_start_points = []
        self.__points = []
        self.__lines = []
        self.__cells = []

        # create all points, lines and cells in the maze.
        for row in range(self.__rows + 1):
            self.__points.append([])
            for column in range(self.__columns + 1):
                self.__points[row].append(Point(self.__margin + column * self.__cell_size, self.__margin + row * self.__cell_size, column, row))

        for row in range(self.__rows + 1):
            self.__lines.append([])
            for column in range(self.__columns + 1):
                self.__lines[row].append([])
                if column < self.__columns:
                    self.__lines[row][column].append(Line(self.__window, self.__points[row][column], self.__points[row][column + 1]))
                else:
                    self.__lines[row][column].append(None)
                if row < self.__rows:
                    self.__lines[row][column].append(Line(self.__window, self.__points[row][column], self.__points[row + 1][column]))
                else:
                    self.__lines[row][column].append(None)

        for row in range(self.__rows):
            self.__cells.append([])
            for column in range(self.__columns):
                self.__cells[row].append(Cell(
                    self.__lines[row][column][0],
                    self.__lines[row][column + 1][1],
                    self.__lines[row + 1][column][0],
                    self.__lines[row][column][1],
                    column,
                    row,
                ))

    def generate_maze(self):
        # randomise entry and exit.
        def get_random_wall():
            side = random.randrange(0, 4)
            if side == 0:
                cell = self.__cells[0][random.randrange(0, self.__columns)]
            elif side == 1:
                cell = self.__cells[random.randrange(0, self.__rows)][self.__columns - 1]
            elif side == 2:
                cell = self.__cells[self.__rows - 1][random.randrange(0, self.__columns)]
            elif side == 3:
                cell = self.__cells[random.randrange(0, self.__rows)][0]
            return cell, side
        
        start_cell, start_side = get_random_wall()
        end_cell, end_side = get_random_wall()
        
        while start_cell == end_cell and start_side == end_side:
            end_cell, end_side = get_random_wall()
        
        def remove_wall(cell: Cell, side: int):
            if side == 0:
                cell.north.exists = False
            elif side == 1:
                cell.east.exists = False
            elif side == 2:
                cell.south.exists = False
            elif side == 3:
                cell.west.exists = False

        remove_wall(start_cell, start_side)
        remove_wall(end_cell, end_side)

        # create maze by moving from current cell to unvisited adjacent cells randomly knocking down walls.
        # when no unvisited adjacent cells remain, look for unvisited cells from the previous cell repeatedly until none can be found.
        def move_cell_recursive(cell: Cell):
            cell.visited = True
            explored_direction = []
            while len(explored_direction) < 4:
                move_direction = random.randrange(0, 4)
                while move_direction in explored_direction:
                    move_direction = random.randrange(0, 4)
                if move_direction == 0 and cell.index_y > 0 and not self.__cells[cell.index_y - 1][cell.index_x].visited:
                    cell.north.exists = False
                    move_cell_recursive(self.__cells[cell.index_y - 1][cell.index_x])
                elif move_direction == 1 and cell.index_x < self.__columns - 1 and not self.__cells[cell.index_y][cell.index_x + 1].visited:
                    cell.east.exists = False
                    move_cell_recursive(self.__cells[cell.index_y][cell.index_x + 1])
                elif move_direction == 2 and cell.index_y < self.__rows - 1 and not self.__cells[cell.index_y + 1][cell.index_x].visited:
                    cell.south.exists = False
                    move_cell_recursive(self.__cells[cell.index_y + 1][cell.index_x])
                elif move_direction == 3 and cell.index_x > 0 and not self.__cells[cell.index_y][cell.index_x - 1].visited:
                    cell.west.exists = False
                    move_cell_recursive(self.__cells[cell.index_y][cell.index_x - 1])
                else:
                    explored_direction.append(move_direction)
                
        move_cell_recursive(start_cell)

        # define where to start drawing the maze from.
        def set_drawing_start_points(cell: Cell, side: int):
            if side == 0:
                self.__draw_start_points.append(cell.north.p0)
                self.__draw_start_points.append(cell.north.p1)
            elif side == 1:
                self.__draw_start_points.append(cell.east.p0)
                self.__draw_start_points.append(cell.east.p1)
            elif side == 2:
                self.__draw_start_points.append(cell.south.p0)
                self.__draw_start_points.append(cell.south.p1)
            elif side == 3:
                self.__draw_start_points.append(cell.west.p0)
                self.__draw_start_points.append(cell.west.p1)

        set_drawing_start_points(start_cell, start_side)

    def draw(self):
        draw_points = self.__draw_start_points
        draw_points_next = []
        to_draw = [] 
        to_draw_next = []

        def get_lines_to_draw():
            for p in draw_points:
                if p.index_x < self.__columns and not self.__lines[p.index_y][p.index_x][0].drawn:
                    to_draw.append([self.__lines[p.index_y][p.index_x][0], 1])
                    draw_points_next.append(self.__points[p.index_y][p.index_x + 1])
                if p.index_y < self.__rows and not self.__lines[p.index_y][p.index_x][1].drawn:
                    to_draw.append([self.__lines[p.index_y][p.index_x][1], 1])
                    draw_points_next.append(self.__points[p.index_y + 1][p.index_x])
                if p.index_x > 0 and not self.__lines[p.index_y][p.index_x - 1][0].drawn:
                    to_draw.append([self.__lines[p.index_y][p.index_x - 1][0], -1])
                    draw_points_next.append(self.__points[p.index_y][p.index_x - 1])
                if p.index_y > 0 and not self.__lines[p.index_y - 1][p.index_x][1].drawn:
                    to_draw.append([self.__lines[p.index_y - 1][p.index_x][1], -1])
                    draw_points_next.append(self.__points[p.index_y - 1][p.index_x])
        
        get_lines_to_draw()


        while len(to_draw):
            lines_in_draw_cycle = [len(to_draw)]
            for line in to_draw:
                self.__window.draw_line(line[0], line[1], lines_in_draw_cycle)
                line[0].drawn = True

            self.__window.wait_animation()
            draw_points = draw_points_next
            draw_points_next = []
            to_draw = []
            get_lines_to_draw()

class Point:
    def __init__(self, x: int, y: int, index_x: int, index_y: int):
        self.x = x
        self.y = y
        self.index_x = index_x
        self.index_y = index_y

class Line:
    def __init__(self, window: Window, p0: Point, p1: Point):
        self.p0 = p0
        self.p1 = p1
        self.line = window.add_line(self)
        self.drawn = False
        self.exists = True

class Cell:
    def __init__(self, north: Line, east: Line, south: Line, west: Line, index_x: int, index_y: int):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.index_x = index_x
        self.index_y = index_y
        self.visited = False