from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
import copy
import random


BOARDSIZE = 81


def issafe(board: List[int], index: int, value: int):
    if len(board) != BOARDSIZE:
        raise ValueError("invalid sudoku board")

    if 1 > value or value > 9:
        raise ValueError("invalid cell value for sudoku")

    if 0 > index or index >= BOARDSIZE:
        raise ValueError("index out of range")

    x = index % 9
    y = index // 9

    for i in range(9):
        ix = x + 9 * i
        iy = i + 9 * y

        if (ix != index and board[ix] == value) or (iy != index and board[iy] == value):
            return False

    x = x - x % 3
    y = y - y % 3

    for i in range(x, x + 3):
        for j in range(y, y + 3):
            indx = i + 9 * j
            if indx != index and board[indx] == value:
                return False

    return True


def solverecursive(board: List[int], fromindex: int, order=[i for i in range(1, 10)]) -> Tuple[bool, List[int]]:
    if len(board) != BOARDSIZE:
        raise ValueError(f"invalid sudoku board. {len(board)} instead of BOARDSIZE")

    if len(order) != 9:
        raise ValueError('invalid number of order elements')

    if 0 > fromindex or fromindex > BOARDSIZE:
        raise ValueError("index out of range")

    while (fromindex < BOARDSIZE and board[fromindex] > 0):
        fromindex += 1

    if (fromindex == BOARDSIZE):
        return True, board

    for i in order:
        if issafe(board, fromindex, i):
            board[fromindex] = i
            solved, newboard = solverecursive(board, fromindex + 1)

            if solved:
                return True, newboard
            else:
                board[fromindex] = 0

    return False, board


def solve(board: List[int]) -> Tuple[bool, List[int]]:
    if len(board) != BOARDSIZE:
        raise ValueError(f"invalid sudoku board. {len(board)} instead of BOARDSIZE")

    return solverecursive(copy.deepcopy(board), 0)


def printboard(board: List[int]):  # pragma: no cover
    if len(board) != BOARDSIZE:
        raise ValueError(f"invalid sudoku board. {len(board)} instead of BOARDSIZE")

    print('[')
    for i in range(0, BOARDSIZE, 9):
        inners = ', '.join([str(i) for i in board[i:i+9]])

        print(f"{inners}{', ' if i < BOARDSIZE-9 else ''}")

    print(']')


def checkboard(board: List[int]) -> bool:
    for i in range(BOARDSIZE):
        if not issafe(board, i, board[i]):
            return False

    return True


def hassinglesolution(board: List[int]) -> bool:
    if len(board) != BOARDSIZE:
        raise ValueError(f"invalid sudoku board. {len(board)} instead of BOARDSIZE")

    solvedincreasing, solutionincreasing = solverecursive(
        copy.deepcopy(board),
        0,
        [i for i in range(1, 10, 1)]
    )

    solveddecreasing, solutiondecreasing = solverecursive(
        copy.deepcopy(board),
        0,
        [i for i in range(9, 0, -1)]
    )

    return solveddecreasing and solvedincreasing and solutionincreasing == solutiondecreasing


def createrandomsolution() -> List[int]:
    board = [0 for _ in range(BOARDSIZE)]

    order = [i for i in range(1, 10, 1)]
    random.shuffle(order)

    _, output = solverecursive(board, 0, order)

    return output


def createpuzzle(tries: int = 3) -> Tuple[List[int], List[int]]:
    board = createrandomsolution()
    solution = copy.deepcopy(board)

    index = 0
    tried = 0

    while tried < tries:
        index = random.randint(0, BOARDSIZE-1)
        board[index] = 0
        if not hassinglesolution(board):
            board[index] = solution[index]
            tried += 1

    board[index] = solution[index]

    return board, solution

    print()
    printboard(solution)
