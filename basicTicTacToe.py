from board import Board
from collections import defaultdict


def boardWinning(board, player='X'):
    isWon, winner = board.whoWon()
    if isWon:
        winProbability = 1 if winner == player else -1
        return winProbability
    else:
        if board.isFull():
            winProbability = 0
            return winProbability

    winProbability = 0.0

    # Memoize by the spaces array since I'm not sure how instances will be cached
    # I think there's a "magic method" that can solve this problem but for now
    # let's do it the easy way
    if tuple(board.spaces) not in boardWinning.probabilities:
        possibleMoves = board.possibleMoves()
        for nextBoard in possibleMoves:
            winProbability += boardWinning(nextBoard, player)

        boardWinning.probabilities[tuple(board.spaces)] = (winProbability / len(possibleMoves))
        return (winProbability / len(possibleMoves))
    else:
        return boardWinning.probabilities[tuple(board.spaces)]

boardWinning.probabilities = defaultdict(list)

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

#runTests()


class TicTacToeGame(object):
    def __init__(self, player='X'):
        self.board = Board()
        self.turn = 'X'
        self.player = player

    def play(self):
        isWon = False
        while not isWon:
            # if this evaluates to True, then isWon must be False
            # so we have a cat's game
            if self.board.isFull():
                winner = "The cat"
                break

            print self.board.prettyPrint()
            self.board = self.nextMove()
            isWon, winner = self.board.whoWon()

        print "Game was won by %s" % winner

    def nextMove(self):
        if self.turn == self.player:
            bestMove = None
            # starting with -1 so we'll definitely replace it
            bestMoveProbabilityOfWinning = -1
            for board in self.board.possibleMoves():
                pWinning = boardWinning(board, self.player)
                print pWinning
                if pWinning > bestMoveProbabilityOfWinning:
                    print "%f better than %f" % (pWinning, bestMoveProbabilityOfWinning)
                    bestMoveProbabilityOfWinning = pWinning
                    bestMove = board
            nextBoard = bestMove
        else:
            validMove = False
            newBoardSpaces = self.board.spaces[:]
            while not validMove:
                spaceIndex = int(raw_input("What space do you want to play in? "))
                if spaceIndex < 1 or spaceIndex > 9:
                    print "Please select a valid space"
                else:
                    spaceIndex -= 1  # map index to board array
                    if self.board.spaces[spaceIndex]:
                        print "That space is full!"
                    else:
                        validMove = True
                        # Player is 'O' if AI is 'X' and vice versa
                        newBoardSpaces[spaceIndex] = 'O' if self.player == 'X' else 'X'
                        nextBoard = Board(newBoardSpaces)

        self.turn = 'O' if self.turn == 'X' else 'X'
        return nextBoard

newGame = TicTacToeGame('O')
newGame.play()