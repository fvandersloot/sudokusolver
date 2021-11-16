from typing import List, Tuple


def issafe(board: List[int], index: int, value: int):
    if len(board) != 81:
        raise ValueError("invalid sudoku board")

    if 1 > value or value > 9:
        raise ValueError("invalid cell value for sudoku")

    if 0 > index or index >= 81:
        raise ValueError("index out of range")

    x = index % 9
    y = index // 9

    for i in range(9):
        ix = x + 9*i
        iy = i + 9*y

        if (ix != index and board[ix] == value) or (iy != index and board[iy] == value):
            return False

    x = x - x % 3
    y = y - y % 3

    for xoff in range(3):
        for yoff in range(3):
            i = x + xoff + 9 * (y + yoff)
            if i != index and board[i] == value:
                return False

    return True


def solverecursive(board: List[int], fromindex: int) -> Tuple[bool, list[int]]:
    if len(board) != 81:
        raise ValueError(f"invalid sudoku board. {len(board)} instead of 81")

    if 0 > fromindex or fromindex > 81:
        raise ValueError("index out of range")

    while (fromindex < 81 and board[fromindex] > 0):
        fromindex += 1

    if (fromindex == 81):
        return True, board

    for i in range(1, 10):
        if issafe(board, fromindex, i):
            board[fromindex] = i
            solved, newboard = solverecursive(board, fromindex + 1)

            if solved:
                return True, newboard
            else:
                board[fromindex] = 0

    return False, board


def solve(board: List[int]) -> Tuple[bool, list[int]]:
    if len(board) != 81:
        raise ValueError(f"invalid sudoku board. {len(board)} instead of 81")

    return solverecursive(board, 0)


def printboard(board: List[int]):
    if len(board) != 81:
        raise ValueError(f"invalid sudoku board. {len(board)} instead of 81")

    print('[')
    for i in range(0, 81, 9):
        inners = ', '.join(board[i:i+9])

        print(f"{inners}{', ' if i < 81-9 else ''}")

    print(']')


def checkboard(board: List[int]) -> bool:
    for i in range(81):
        if not issafe(board, i, board[i]):
            return False

    return True


if __name__ == "__main__":

    board = [
        0, 0, 0, 8, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 4, 3,
        5, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 7, 0, 8, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 2, 0, 3, 0, 0, 0, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 7, 5,
        0, 0, 3, 4, 0, 0, 0, 0, 0,
        0, 0, 0, 2, 0, 0, 6, 0, 0
    ]

    printboard(board)

    solved, solution = solve(board)

    print()
    print(f"solution {'is' if checkboard(solution) else 'isnt'} safe")
    printboard(solution)
    print(solved)
