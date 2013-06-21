class Board(object):

    def __init__(self, spaces=None):
        self.spaces = spaces[:] if spaces else [None for i in range(9)]

        self.isXTurn = True

    def __str__(self):
        return self.spaces.__str__()

    def possibleMoves(self):
        moves = []
        for i, space in enumerate(self.spaces):
            if not space:
                nextBoard = self.spaces[:]
                nextBoard[i] = 'X' if self.isXTurn else 'O'
                newBoard = Board(nextBoard)
                newBoard.isXTurn = False if self.isXTurn else True
                moves.append(newBoard)
        return moves

    def isFull(self):
        for space in self.spaces:
            if not space:
                return False
        return True

    def whoWon(self):

        def rowWin(player):
            for i in range(3):
                if len([True for j in self.getRow(i) if j == player]) == 3:
                    return True
            return False

        def columnWin(player):
            for i in range(3):
                if len([True for j in self.getColumn(i) if j == player]) == 3:
                    return True
            return False

        def diagWin(player):
            for i in range(2):
                if len([True for j in self.getDiag(i) if j == player]) == 3:
                    return True
            return False

        xWon = (rowWin('X') or columnWin('X') or diagWin('X'))
        oWon = (rowWin('O') or columnWin('O') or diagWin('O'))

        if xWon or oWon:
            if xWon:
                return (True, 'X')
            elif oWon:
                return (True, 'O')
            else:
                return (False, None)
        else:
            return (False, None)

    def getRow(self, r):
        if r > 2:
            return None

        start = r * 3
        return self.spaces[start:start + 3]

    def getColumn(self, c):
        if c > 2:
            return None

        start = c
        return [self.spaces[start + i * 3] for i in range(3)]

    def getDiag(self, d):

        if d > 1:
            return None

        start = 2 * d
        step = 4 - start
        return [self.spaces[start + step * i] for i in range(3)]


def boardWinning(board, player='X'):
    isWon, winner = board.whoWon()
    if isWon:
        winProbability = 1 if winner == player else 0
        return winProbability
    else:
        if board.isFull():
            winProbability = 0
            return winProbability

    winProbability = 0.0

    possibleMoves = board.possibleMoves()
    for nextBoard in possibleMoves:
        winProbability += boardWinning(nextBoard, player)

    return (winProbability / len(possibleMoves))


def runTests():
    print 'running Tests For Board 1'
    board1 = Board(['X', None, 'O', 'O', 'X', 'X', None, 'X', 'O'])
    assert boardWinning(board1, 'X') == 0.5
    assert boardWinning(board1, 'O') == 0.0
    print 'running Tests For Board 2'
    board2 = Board(['X', 'O', 'O', 'O', 'X', 'X', 'X', 'X', 'O'])
    assert boardWinning(board2, 'X') == 0.0
    assert boardWinning(board2, 'O') == 0.0
    board3 = Board([None, None, 'O', 'O', 'X', 'X', None, 'X', 'O'])
    print 'running Tests For Board 3'
    assert boardWinning(board3, 'X') == 2.0 / 3.0
    assert boardWinning(board3, 'O') == 0.0

runTests()
