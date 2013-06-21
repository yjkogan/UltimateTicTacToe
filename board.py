class Board(object):

    def __init__(self, spaces=None):
        self.spaces = spaces[:] if spaces else [None for i in range(9)]

        self.isXTurn = True

    def __str__(self):
        return self.spaces.__str__()

    def prettyPrint(self):
        for i in range(3):
            r = self.getRow(i)
            for j, c in enumerate(r):
                if c:
                    print c,
                else:
                    # add one to the index for easy of understanding
                    print j + i * 3 + 1,
                if j != len(r) - 1:
                    print '|',
            print ''

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

    # I think there's probably a more efficient way of computing this
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