import random
from collections import deque

def shuffle(array):
    """Shuffle a list randomly."""
    for currentIndex in range(len(array)):
        # shuffle each number with a random number from another index
        randomIndex = int(random.random() * currentIndex)
        array[currentIndex], array[randomIndex] = array[randomIndex], array[currentIndex]
    return array

def getSeen(board, x, y):
    """Get all the numbers seen in the same row, column, and box region."""
    
    # add all numbers in the same row and column
    seen = set(board[x]) | set(board[i][y] for i in range(9))

    # add all numbers in the same box region
    startX, startY = (x // 3) * 3, (y // 3) * 3
    for i in range(startX, startX + 3):
        for j in range(startY, startY + 3):
            seen.add(board[i][j])

    # 0 is empty slot, it can be removed
    if 0 in seen:
        seen.remove(0)

    return seen

def generateSolution():
    """Generate a solved Sudoku board."""
    def createSolution(idx = 0):
        if idx == 81:
            # when reached 81 in backtracking, then a solution is found
            return True

        x, y = divmod(idx, 9)
        seen = getSeen(board, x, y)
        # in the current slot, try each numbers from 1..9
        for n in shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9]):
            # if this number is valid number of the slot, continue to the next one
            if n not in seen:
                board[x][y] = n
                # once a solution is found, we can stop looking further
                if createSolution(idx + 1):
                    return True
                board[x][y] = 0
        # if we tried all numbers in this slot then there's no solutions
        return False

    board = [[" " for _ in range(9)] for _ in range(9)]
    createSolution()
    return board

def generatePuzzle(board, n):
    """Generate a Sudoku puzzle from the solved board. n is the difficulty from 1-4."""
    assert 1 <= n <= 5

    # check if the board still creates a unique solution
    # after filling the covered up the board
    def isBoardUnique():
        numSolutions = 0
        def _isBoardUnique(idx = 0):
            nonlocal numSolutions
            # once all slots are filled, then one possible solution is found
            if idx == 81:
                numSolutions += 1
                return

            x, y = divmod(idx, 9)
            # if the current slot is covered up, try to fill it using back tracking
            if board[x][y] == 0:
                seen = getSeen(board, x, y)
                for n in shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9]):
                    if n not in seen:
                        board[x][y] = n
                        _isBoardUnique(idx + 1)
                        board[x][y] = 0
                        if numSolutions > 1:
                            return
            # if the current slot is not covered, then proceed to next
            else:
                _isBoardUnique(idx + 1)
        
        _isBoardUnique()
        return numSolutions == 1

    # create a deep copy of board
    board = [row.copy() for row in board]
    
    # put each box region as a queue
    regions = [deque() for _ in range(9)]
    for idx in range(81):
        i, j = idx // 9, idx % 9
        regions[i // 3 * 3 + j // 3].append([i, j])

    # shuffle each queue
    for i in range(9):
        shuffle(regions[i])

    # evenly cover up each box region for the solution, and ensure
    # the final board only contains one unique solution
    for i in range(9 * n + 2):
        x, y = regions[i % 9].popleft()
        regions[i % 9].append([x, y])
        cur = board[x][y]
        board[x][y] = 0
        # if the covered board is not unique, continue to the next region
        if not isBoardUnique():
            board[x][y] = cur

    return board

def print_sudoku(board):
    '''Print Sudoku board'''
    res = []
    for i, row in enumerate(board):
        res.append(' ')
        for j, num in enumerate(row):
            num = str(num) if num != 0 else ' '
            res.append(num + (' ' if j < 9 else ''))
            if j in [2, 5]:
                res.append('| ')
        res.append('\n')
        
        if i in [2, 5]:
            for j in range(23):
                res.append('+' if j in [7, 15] else '-')
            res.append('\n')
    print('\n' + ''.join(res))

if __name__ == '__main__':
    while True:
        try:
            level = input('\nPlease select difficulty(1-5): ')
            board = generateSolution()
            covered_board = generatePuzzle(board, int(level))

            print('\nPuzzle:')
            print_sudoku(covered_board)

            print('-' * 23 + '\n\nSolution:')
            print_sudoku(board)

        except Exception:
            pass
