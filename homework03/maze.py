import random
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(
    rows: int = 15,
    cols: int = 15,
) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[
        List[
            Union[
                str,
                int,
            ]
        ]
    ],
    coord: Tuple[int, int],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    choice = [
        "up",
        "right",
    ]
    x, y = (
        coord[0],
        coord[1],
    )
    route = random.choice(choice)
    if route == "up":
        if x != 1:
            grid[x - 1][y] = " "
        elif y + 2 != len(grid[0]):
            grid[x][y + 1] = " "
    else:
        if y + 2 != len(grid[0]):
            grid[x][y + 1] = " "
        elif x != 1:
            grid[x - 1][y] = " "
    return grid


def bin_tree_maze(
    rows: int = 15,
    cols: int = 15,
    random_exit: bool = True,
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(
        rows,
        cols,
    )
    empty_cells = []
    for (
        x,
        row,
    ) in enumerate(grid):
        for (
            y,
            _,
        ) in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append(
                    (
                        x,
                        y,
                    )
                )

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for i in empty_cells:
        grid = remove_wall(grid, i)

    # генерация входа и выхода
    if random_exit:
        (
            x_in,
            x_out,
        ) = randint(
            0,
            rows - 1,
        ), randint(
            0,
            rows - 1,
        )
        y_in = (
            randint(
                0,
                cols - 1,
            )
            if x_in
            in (
                0,
                rows - 1,
            )
            else choice(
                (
                    0,
                    cols - 1,
                )
            )
        )
        y_out = (
            randint(
                0,
                cols - 1,
            )
            if x_out
            in (
                0,
                rows - 1,
            )
            else choice(
                (
                    0,
                    cols - 1,
                )
            )
        )
    else:
        (
            x_in,
            y_in,
        ) = (
            0,
            cols - 2,
        )
        (
            x_out,
            y_out,
        ) = (
            rows - 1,
            1,
        )

    (
        grid[x_in][y_in],
        grid[x_out][y_out],
    ) = ("X", "X")

    return grid


def get_exits(
    grid: List[
        List[
            Union[
                str,
                int,
            ]
        ]
    ]
) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    rows = len(grid) - 1
    cols = len(grid[0]) - 1
    coordinates = []
    for i in range(cols):
        if grid[0][i] == "X":
            coordinates.append(
                (
                    0,
                    i,
                )
            )
        if grid[len(grid[0]) - 1][i] == "X":
            coordinates.append(
                (
                    len(grid[0]) - 1,
                    i,
                )
            )
    for i in range(rows):
        if grid[i][0] == "X":
            coordinates.append(
                (
                    i,
                    0,
                )
            )
        if grid[i][len(grid) - 1] == "X":
            coordinates.append(
                (
                    i,
                    len(grid) - 1,
                )
            )
    if len(coordinates) > 1:
        if coordinates[0][0] > coordinates[1][0]:
            (
                coordinates[0],
                coordinates[1],
            ) = (
                coordinates[1],
                coordinates[0],
            )
    return coordinates


def make_step(
    grid: List[
        List[
            Union[
                str,
                int,
            ]
        ]
    ],
    k: int,
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    ways = [
        [0, 1],
        [1, 0],
        [0, -1],
        [-1, 0],
    ]
    actual_cell = []
    actual_coefficient = []
    for rows in range(len(grid)):
        for cols in range(len(grid[0])):
            if grid[rows][cols] == k:
                actual_cell.append(
                    (
                        rows,
                        cols,
                    )
                )
                actual_coefficient.append(k + 1)
    while actual_cell and actual_coefficient:
        cell_x = actual_cell[0][0]
        cell_y = actual_cell[0][1]
        for (
            x,
            y,
        ) in ways:
            if 0 <= cell_x + x < len(grid) and 0 <= cell_y + y < len(grid[0]):
                if grid[cell_x + x][cell_y + y] == 0:
                    grid[cell_x + x][cell_y + y] = actual_coefficient[0]
        actual_cell.pop(0)
        actual_coefficient.pop(0)
    return grid


def shortest_path(
    grid: List[
        List[
            Union[
                str,
                int,
            ]
        ]
    ],
    exit_coord: Tuple[int, int],
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int,]],]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x = exit_coord[0]
    y = exit_coord[1]
    k = grid[x][y]
    moves = [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0],
    ]
    way = [(x, y)]
    while k != 1:
        for (
            x_move,
            y_move,
        ) in moves:
            if 0 <= x + x_move < len(grid) and 0 <= y + y_move < len(grid[0]):
                next_cell = grid[x + x_move][y + y_move]
                if type(next_cell) == int:
                    if next_cell < int(k):
                        (
                            x,
                            y,
                        ) = (
                            x + x_move,
                            y + y_move,
                        )
                        way.append(
                            (
                                x,
                                y,
                            )
                        )
                        k = grid[x][y]

    for i in range(len(grid) - 1):
        for j in range(len(grid[0])):
            if grid[i][j] != "■":
                grid[i][j] = " "

    return way


def encircled_exit(
    grid: List[
        List[
            Union[
                str,
                int,
            ]
        ]
    ],
    coord: Tuple[int, int],
) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    if (
        coord
        in (
            (0, 0),
            (
                len(grid) - 1,
                len(grid) - 1,
            ),
            (
                len(grid) - 1,
                0,
            ),
            (
                0,
                len(grid) - 1,
            ),
        )
        or coord[0] == 0
        and grid[1][coord[1]] != " "
        or coord[0] == len(grid) - 1
        and grid[len(grid) - 2][coord[1]] != " "
        or coord[1] == 0
        and grid[coord[0]][1] != " "
        or coord[1] == len(grid) - 1
        and grid[coord[0]][len(grid) - 2] != " "
    ):
        return True
    else:
        return False


def solve_maze(
    grid: List[
        List[
            Union[
                str,
                int,
            ]
        ]
    ],
) -> Tuple[List[List[Union[str, int,]]], Optional[Union[Tuple[int, int,], List[Tuple[int, int,]],]],]:
    """

    :param grid:
    :return:
    """

    doors = get_exits(grid)
    if len(doors) < 2:
        return (
            grid,
            doors[0],
        )
    else:
        for door in doors:
            if encircled_exit(
                grid,
                door,
            ):
                return (
                    grid,
                    None,
                )
    enter = doors[0]
    exit = doors[1]
    if exit[1] - enter[1] == 1 and exit[0] - enter[0] == 0:
        return (
            grid,
            doors[::-1],
        )
    elif exit[1] - enter[1] == 0 and exit[0] - enter[0] == 1:
        return (
            grid,
            doors[::-1],
        )
    elif exit[0] - enter[0] == 0 and exit[1] - enter[1] == 1:
        return (
            grid,
            doors[::-1],
        )
    elif exit[0] - enter[0] == 1 and exit[1] - enter[1] == 0:
        return (
            grid,
            doors[::-1],
        )

    grid[doors[0][0]][doors[0][1]] = 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == " ":
                grid[i][j] = 0
            elif grid[i][j] == "X":
                grid[i][j] = 0

    k = 1
    while grid[doors[1][0]][doors[1][1]] == 0:
        grid = make_step(grid, k)
        k += 1

    path = shortest_path(
        grid,
        doors[1],
    )

    return (
        grid,
        path,
    )


def add_path_to_grid(
    grid: List[
        List[
            Union[
                str,
                int,
            ]
        ]
    ],
    path: Optional[
        Union[
            Tuple[
                int,
                int,
            ],
            List[
                Tuple[
                    int,
                    int,
                ]
            ],
        ]
    ],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for (
            i,
            row,
        ) in enumerate(grid):
            for (
                j,
                _,
            ) in enumerate(row):
                if (
                    i,
                    j,
                ) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(
        pd.DataFrame(
            bin_tree_maze(
                15,
                15,
            )
        )
    )
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    (
        _,
        PATH,
    ) = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
