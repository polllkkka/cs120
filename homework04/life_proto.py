import pygame
from pygame.locals import *
import typing as tp
from random import randint

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Матрица значений клеток
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = randint(0, 1)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            y = i * self.cell_size
            for j in range(self.cell_width):
                x = j * self.cell_size
                color = pygame.Color("green" if self.grid[i][j] else "white")
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        i, j = cell
        cells = []
        if i > 0:
            if j > 0:
                cells.append(self.grid[i - 1][j - 1])
            cells.append(self.grid[i - 1][j])
            if j < self.cell_width - 1:
                cells.append(self.grid[i - 1][j + 1])

        if j > 0:
            cells.append(self.grid[i][j - 1])
        if j < self.cell_width - 1:
            cells.append(self.grid[i][j + 1])

        if i < self.cell_height - 1:
            if j > 0:
                cells.append(self.grid[i + 1][j - 1])
            cells.append(self.grid[i + 1][j])
            if j < self.cell_width - 1:
                cells.append(self.grid[i + 1][j + 1])

        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                alive_neighbours_quantity = self.get_neighbours((i, j)).count(1)
                if alive_neighbours_quantity == 3 or alive_neighbours_quantity == 2 and self.grid[i][j]:
                    grid[i][j] = 1
        self.grid = grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
