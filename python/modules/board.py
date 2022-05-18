class Board():
    def __init__(self):
        self.board = [['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', 'c', ' ', ' ', ' ', ' ', ' ', 'c', ' '],
                      ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' ', 'p'],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      ['P', ' ', 'P', ' ', 'P', ' ', 'P', ' ', 'P'],
                      [' ', 'C', ' ', ' ', ' ', ' ', ' ', 'C', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']]
    
    def FEN(self):
        retstr = ""
        for i in range(9):
            if i != 0:
                retstr += '/'
            cnt = 0
            for j in range(10):
                if self.board[i][j] == ' ':
                    cnt += 1
                else:
                    if cnt != 0:
                        retstr += str(cnt)
                    retstr += self.board[i][j]
        return retstr

    def getPiecebyCoor(self, coor):
        x = ord(coor[0]) - ord('a')
        y = ord(coor[1]) - ord('0')
        if x < 0 or x > 8 or y < 0 or y > 9:
            return False
        return self.board[y][x]
    
    def move(self, coor1, coor2):
        x1 = ord(coor1[0]) - ord('a')
        y1 = ord(coor1[1]) - ord('0')
        x2 = ord(coor2[0]) - ord('a')
        y2 = ord(coor2[1]) - ord('0')
        tmpPiece = self.board[y2][x2]
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = ' '
        return tmpPiece