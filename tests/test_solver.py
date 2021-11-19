from typing import List, Tuple
from solver.solver import BOARDSIZE, checkboard, createpuzzle, createrandomsolution, hassinglesolution, issafe, solve, solverecursive
import pytest

#     0  1  2  3  4  5  6  7  8
#   *--+--+--*--+--+--*--+--+--*
# 0 | 0| 1| 2| 3| 4| 5| 6| 7| 8|
#   +--+--+--+--+--+--+--+--+--+
# 1 | 9|10|11|12|13|14|15|16|17|
#   +--+--+--+--+--+--+--+--+--+
# 2 |18|19|20|21|22|23|24|25|26|
#   *--+--+--*--+--+--*--+--+--*
# 3 |27|28|29|30|31|32|33|34|35|
#   +--+--+--+--+--+--+--+--+--+
# 4 |36|37|38|39|40|41|42|43|44|
#   +--+--+--+--+--+--+--+--+--+
# 5 |45|46|47|48|49|50|51|52|53|
#   *--+--+--*--+--+--*--+--+--*
# 6 |54|55|56|57|58|59|60|61|62|
#   +--+--+--+--+--+--+--+--+--+
# 7 |63|64|65|66|67|68|69|70|71|
#   +--+--+--+--+--+--+--+--+--+
# 8 |72|73|74|75|76|77|78|79|80|
#   *--+--+--*--+--+--*--+--+--+

DATA: List[Tuple[List[int], List[int], bool]] = [(
    [
        0, 0, 0, 9, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 7, 0, 0, 0, 0,
        0, 0, 0, 5, 0, 8, 4, 0, 3,
        1, 0, 5, 4, 0, 0, 9, 0, 7,
        0, 0, 6, 0, 0, 0, 0, 0, 0,
        7, 0, 0, 0, 0, 3, 0, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 8, 2, 0, 3, 1,
        0, 0, 8, 3, 9, 0, 0, 7, 0
    ], [
        5, 8, 2, 9, 3, 4, 7, 1, 6,
        3, 6, 4, 2, 7, 1, 8, 5, 9,
        9, 7, 1, 5, 6, 8, 4, 2, 3,
        1, 3, 5, 4, 2, 6, 9, 8, 7,
        8, 2, 6, 7, 1, 9, 3, 4, 5,
        7, 4, 9, 8, 5, 3, 1, 6, 2,
        6, 5, 3, 1, 4, 7, 2, 9, 8,
        4, 9, 7, 6, 8, 2, 5, 3, 1,
        2, 1, 8, 3, 9, 5, 6, 7, 4
    ], True), ([
        0, 0, 0, 8, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 4, 3,
        5, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 7, 0, 8, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 2, 0, 3, 0, 0, 0, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 7, 5,
        0, 0, 3, 4, 0, 0, 0, 0, 0,
        0, 0, 0, 2, 0, 0, 6, 0, 0
    ], [
        2, 3, 4, 8, 5, 1, 7, 6, 9,
        1, 6, 8, 7, 2, 9, 5, 4, 3,
        5, 7, 9, 6, 4, 3, 2, 1, 8,
        3, 1, 6, 9, 7, 4, 8, 5, 2,
        4, 9, 7, 5, 8, 2, 1, 3, 6,
        8, 2, 5, 3, 1, 6, 4, 9, 7,
        6, 4, 2, 1, 9, 8, 3, 7, 5,
        7, 8, 3, 4, 6, 5, 9, 2, 1,
        9, 5, 1, 2, 3, 7, 6, 8, 4
    ], False)
]


def test_movechecker():
    board = [1 if i == 1 else 0 for i in range(81)]

    # Testcase: adding a number that would create a conflict
    assert not issafe(board, 0, 1)

    # Testcase: adding a number that would not create a conflict
    assert issafe(board, 0, 2)

    # Testcase: calling function on board of invalid size
    with pytest.raises(ValueError):
        issafe([], 0, 1)

    # Testcase: calling function on non-existent tile
    with pytest.raises(ValueError):
        issafe(board, BOARDSIZE, 1)

    # Testcase: calling function with invalid value
    with pytest.raises(ValueError):
        issafe(board, 0, 0)


def test_recursivesolver():
    # Testcase: invalid boardsize
    with pytest.raises(ValueError):
        solverecursive([0, 0], 0)

    # Testcase: invalid index
    emptyboard = [0 for _ in range(BOARDSIZE)]
    with pytest.raises(ValueError):
        solverecursive(emptyboard, BOARDSIZE + 1)

    # Testcase: invaled order length
    with pytest.raises(ValueError):
        solverecursive(emptyboard, 0, [1, 2, 3])

    # Other testcases are coverd in test_solver


def test_solver():
    # Testcase: invalid boardsize
    with pytest.raises(ValueError):
        solve([0, 0])

    for testboard, real_solution, _ in DATA:

        solved, solution = solve(testboard)

        # Testcase: was able to find a solution
        assert solved

        # Testcase: was able to find expected solution
        assert solution == real_solution


def test_boardchecker():
    # Testcase: invalid boardsize
    with pytest.raises(ValueError):
        checkboard([0, 0])

    # Testcase: conflicting board
    board = [i % 9 for i in range(81)]
    assert not checkboard(board)

    # Testcase: non-conflicting board
    for _, solution, _ in DATA:
        assert checkboard(solution)


def test_hassinglesolution():
    # Testcase: invalid boardsize
    with pytest.raises(ValueError):
        hassinglesolution([0, 0])

    for testboard, _, hassingle in DATA:
        # Testcase: check if output matches checked value
        assert hassingle == hassinglesolution(testboard)


def test_boardgeneration():
    board = createrandomsolution()

    # Testcase: generated board is valid
    assert len(board) == BOARDSIZE
    assert checkboard(board)


def test_puzzlegeneration():
    puzzle, solution = createpuzzle(2)

    issolvable, solvedpuzzle = solve(puzzle)

    # Testcase: puzzle is solvable
    assert issolvable

    # Testcase: puzzle is solvable to solution
    assert solvedpuzzle == solution

    # Testcase: puzzle has single solution
    assert hassinglesolution(puzzle)

    # Testcase: all non zero cells in puzzle are the same as in solution
    assert all([v == 0 or v == solution[i] for i, v in enumerate(puzzle)])
