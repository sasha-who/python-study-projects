from enum import Enum

ROW_LENGTH = 3
CELLS_COUNT = 9


class CellValue(Enum):
    CROSS = "X"
    NOUGHT = "O"
    EMPTY = "_"


class Result(Enum):
    DRAW = "Draw"
    IMPOSSIBLE = "Impossible"
    X_WINS = "X wins"
    O_WINS = "O wins"


class CoordinatesError(Enum):
    WRONG_COUNT = "You should enter 2 coordinates!"
    WRONG_RANGE = "Coordinates should be from 1 to 3!"
    WRONG_TYPE = "You should enter numbers!"
    WRONG_CELL = "This cell is occupied! Choose another one!"


rows_list = []
current_step = 1
step_result = ""


def print_grid(rows):
    print("---------")
    for row in rows:
        print("|", " ".join(row), "|")
    print("---------")


def check_coordinates():
    coordinates = input("Enter the coordinates: ").split()
    checked_coordinates = []

    # Check if value is wrong
    if len(coordinates) < 2:
        print(CoordinatesError.WRONG_COUNT.value)
        return False

    for coordinate in coordinates:
        try:
            int_coordinate = int(coordinate)

            if int_coordinate < 1 or int_coordinate > 3:
                print(CoordinatesError.WRONG_RANGE.value)
                return False

            checked_coordinates.append(int_coordinate - 1)
        except ValueError:
            print(CoordinatesError.WRONG_TYPE.value)
            return False

    # Check if cell is not empty
    current_cell = rows_list[checked_coordinates[0]][checked_coordinates[1]]

    if current_cell != CellValue.EMPTY.value:
        print(CoordinatesError.WRONG_CELL.value)
        return False

    return checked_coordinates


def process_step():
    columns_list = [[], [], []]
    diagonals_list = [[], []]
    user_coordinates = False

    print_grid(rows_list)

    # Ask for coordinates until they are correct
    while not user_coordinates:
        user_coordinates = check_coordinates()

    # Find out whose move
    global current_step
    current_player = CellValue.NOUGHT.value if current_step % 2 == 0 else CellValue.CROSS.value
    rows_list[user_coordinates[0]][user_coordinates[1]] = current_player

    # Form columns and diagonals lists
    for row_index, row in enumerate(rows_list):
        for cell_index, cell in enumerate(row):
            columns_list[cell_index].append(cell)
            if row_index == 1 and cell_index == 1:
                diagonals_list[0].append(cell)
                diagonals_list[1].append(cell)
            elif row_index == cell_index:
                diagonals_list[0].append(cell)
            elif abs(row_index - cell_index) == ROW_LENGTH - 1:
                diagonals_list[1].append(cell)

    all_groups = rows_list + columns_list + diagonals_list

    # Check current result
    is_three_x = False
    is_three_o = False

    for group in all_groups:
        unique_group = list(set(group))
        if len(unique_group) == 1:
            if unique_group[0] == CellValue.CROSS.value:
                is_three_x = True
            elif unique_group[0] == CellValue.NOUGHT.value:
                is_three_o = True

    cells_list = [cell for row in rows_list for cell in row]

    x_cells_count = len([x_cell for x_cell in cells_list if x_cell == CellValue.CROSS.value])
    o_cells_count = len([o_cell for o_cell in cells_list if o_cell == CellValue.NOUGHT.value])

    if not is_three_x and not is_three_o:
        if not (CellValue.EMPTY.value in cells_list):
            return Result.DRAW.value
        elif abs(x_cells_count - o_cells_count) > 1:
            return Result.IMPOSSIBLEv
        else:
            current_step += 1
            return
    elif is_three_x and is_three_o:
        return Result.IMPOSSIBLE.value
    elif is_three_x:
        return Result.X_WINS.value
    elif is_three_o:
        return Result.O_WINS.value


# Fill the list of rows with initial values
for index in range(0, CELLS_COUNT, ROW_LENGTH):
    row_list = [CellValue.EMPTY.value for x in range(index, index + ROW_LENGTH)]
    rows_list.append(row_list)

# Go to the next step until there is no final result
while not (step_result in [Result.DRAW.value, Result.X_WINS.value, Result.O_WINS.value]):
    step_result = process_step()

# Print the final state of the grid and the result
print_grid(rows_list)
print(step_result)
