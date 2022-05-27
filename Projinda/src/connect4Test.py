import unittest

import numpy as np

from connect4 import Connect4


class Connect4Test(unittest.TestCase):
    # Returns a board which can be won by placing a "1" in the fourth column, via an ascending diagonal streak
    def getThreeStreakDiagonal(self):
        return np.copy(np.array([[0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 1, 1, 0, 0, 0],
                                 [0, 1, 2, 2, 0, 0, 0],
                                 [1, 2, 2, 1, 2, 0, 0]]))

    # Returns a board which can be won by placing a "1" in the top left corner
    def getThreeStreakCorner(self):
        return np.copy(np.array([[0, 0, 0, 0, 0, 0, 0],
                                 [1, 1, 0, 0, 0, 0, 0],
                                 [2, 2, 1, 2, 0, 0, 0],
                                 [1, 2, 2, 1, 0, 0, 0],
                                 [2, 1, 2, 2, 0, 0, 0],
                                 [1, 2, 1, 1, 0, 0, 0]]))


    # Returns a board where the next move should result in a draw
    def getTiedBoard(self):
        return np.copy(np.array([[1, 2, 1, 2, 1, 1, 0],
                                  [2, 2, 1, 2, 1, 2, 1],
                                  [2, 1, 2, 1, 2, 1, 2],
                                  [1, 1, 2, 1, 2, 1, 2],
                                  [2, 1, 2, 1, 2, 1, 2],
                                  [1, 2, 1, 2, 1, 2, 1]]))

    def setUp(self):
        self.c = Connect4()

    # Tests that four similar markers in a vertical row results in a win
    def test_verticalStreak(self):
        for i in range(4):
            self.c.move(i)
            self.c.move(i)

        self.assertEqual(self.c.getWinner(), 1)

    # Tests that four similar markers in a horizontal row results in a win
    def test_horizontalStreak(self):
        for _ in range(4):
            self.c.move(0)
            self.c.move(1)

        self.assertEqual(self.c.getWinner(), 1)

    # Tests that four similar markers in an ascending diagonal row results in a win
    def test_ascendingDiagonalStreak(self):
        self.c.state = self.getThreeStreakDiagonal()
        self.c.move(3)
        self.assertEqual(self.c.getWinner(), 1)

    # Tests that four similar markers in an descending diagonal row results in a win
    def test_descendingDiagonalStreak(self):
        self.c.state = np.fliplr(self.getThreeStreakDiagonal())
        self.c.move(3)
        self.assertEqual(self.c.getWinner(), 1)

    # Tests the case when one of the markers in a four-marker-long streak are in the corners of the board
    def test_cornerStreak(self):
        # upper left corner
        self.c.state = self.getThreeStreakCorner()
        self.c.move(0)
        self.assertEqual(self.c.getWinner(), 1)

        # upper right corner
        self.c.state = np.fliplr(self.getThreeStreakCorner())
        self.c.move(1)
        self.assertEqual(self.c.getWinner(), 1)

    # Tests that three similar markers in a row does not result in a win
    def test_3inARowDoesNotWin(self):
        for _ in range(3):
            self.c.move(0)
            self.c.move(1)

        self.assertEqual(self.c.getWinner(), -1)

    # New markers are dropped to the lowest available row in their column
    def test_markersAreDroppedCorrectly(self):
        for _ in range(self.c.rows):
            self.c.move(0)
            self.c.switchPlayer()

        expected = [2, 1, 2, 1, 2, 1]
        actual = self.c.state[:, 0]
        self.assertTrue(np.array_equal(actual, expected))

    def test_fullBoardResultsInDraw(self):
        self.c.state = self.getTiedBoard()
        self.c.move(6)
        self.assertEqual(self.c.mode, 1)

    if __name__ == '__main__':
        unittest.main()
