import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)));

from pieces import General, Guardian, Elephant, Horse, Chariot, Cannon, Soldier
from vec2d import Vec2d, Range2d
import copy

def remove(array, element):
    poplist = []
    for i in range(len(array)):
        if element.x == array[i].x and element.y == array[i].y:
            poplist.append(i);
    for i in poplist:
        array.pop(i);
    return array

class Board:
    def __init__(self):
        self.rounds = 0;
        self.turn = "red"
        self.board = [[-1 for j in range(10)] for i in range(9)];
        self.pieces = [General(0, Vec2d(4, 0)),
                       Guardian(1, Vec2d(3, 0)), 
                       Guardian(2, Vec2d(5, 0)),
                       Elephant(3, Vec2d(2, 0)),
                       Elephant(4, Vec2d(6, 0)),
                       Horse(5, Vec2d(1, 0)),
                       Horse(6, Vec2d(7, 0)),
                       Chariot(7, Vec2d(0, 0)),
                       Chariot(8, Vec2d(8, 0)),
                       Cannon(9, Vec2d(1, 2)),
                       Cannon(10, Vec2d(7, 2)),
                       Soldier(11, Vec2d(0, 3)),
                       Soldier(12, Vec2d(2, 3)),
                       Soldier(13, Vec2d(4, 3)),
                       Soldier(14, Vec2d(6, 3)),
                       Soldier(15, Vec2d(8, 3)),
                       General(16, Vec2d(4, 0)),
                       Guardian(17, Vec2d(3, 0)), 
                       Guardian(18, Vec2d(5, 0)),
                       Elephant(19, Vec2d(2, 0)),
                       Elephant(20, Vec2d(6, 0)),
                       Horse(21, Vec2d(1, 0)),
                       Horse(22, Vec2d(7, 0)),
                       Chariot(23, Vec2d(0, 0)),
                       Chariot(24, Vec2d(8, 0)),
                       Cannon(25, Vec2d(1, 2)),
                       Cannon(26, Vec2d(7, 2)),
                       Soldier(27, Vec2d(0, 3)),
                       Soldier(28, Vec2d(2, 3)),
                       Soldier(29, Vec2d(4, 3)),
                       Soldier(30, Vec2d(6, 3)),
                       Soldier(31, Vec2d(8, 3))];
        self.renderPieces();
    
    def reset(self):
        self.rounds = 0;
        self.turn = "red"
        self.board = [[-1 for j in range(10)] for i in range(9)];
        self.pieces = [General(0, Vec2d(4, 0)),
                       Guardian(1, Vec2d(3, 0)), 
                       Guardian(2, Vec2d(5, 0)),
                       Elephant(3, Vec2d(2, 0)),
                       Elephant(4, Vec2d(6, 0)),
                       Horse(5, Vec2d(1, 0)),
                       Horse(6, Vec2d(7, 0)),
                       Chariot(7, Vec2d(0, 0)),
                       Chariot(8, Vec2d(8, 0)),
                       Cannon(9, Vec2d(1, 2)),
                       Cannon(10, Vec2d(7, 2)),
                       Soldier(11, Vec2d(0, 3)),
                       Soldier(12, Vec2d(2, 3)),
                       Soldier(13, Vec2d(4, 3)),
                       Soldier(14, Vec2d(6, 3)),
                       Soldier(15, Vec2d(8, 3)),
                       General(16, Vec2d(4, 0)),
                       Guardian(17, Vec2d(3, 0)), 
                       Guardian(18, Vec2d(5, 0)),
                       Elephant(19, Vec2d(2, 0)),
                       Elephant(20, Vec2d(6, 0)),
                       Horse(21, Vec2d(1, 0)),
                       Horse(22, Vec2d(7, 0)),
                       Chariot(23, Vec2d(0, 0)),
                       Chariot(24, Vec2d(8, 0)),
                       Cannon(25, Vec2d(1, 2)),
                       Cannon(26, Vec2d(7, 2)),
                       Soldier(27, Vec2d(0, 3)),
                       Soldier(28, Vec2d(2, 3)),
                       Soldier(29, Vec2d(4, 3)),
                       Soldier(30, Vec2d(6, 3)),
                       Soldier(31, Vec2d(8, 3))];
        self.renderPieces();
    
    def realPos(self, piece):
        if piece.index < 16:
            return piece.pos;
        else:
            return Vec2d(8 - piece.pos.x, 9 - piece.pos.y);
    
    def logicPos(self, piece):
        if piece.index < 16:
            return piece.pos;
        else:
            return Vec2d(8 - piece.pos.x, 9 - piece.pos.y);
    
    def logicPosIndex(self, index, pos):
        if index < 16:
            return pos;
        else:
            return Vec2d(8 - pos.x, 9 - pos.y);
    
    def renderPieces(self):
        self.board = [[-1 for j in range(10)] for i in range(9)];
        for piece in self.pieces:
            pos = self.realPos(piece)
            if piece.isAlive:
                self.board[pos.x][pos.y] = piece.index;
    
    def isOpponent(self, piece, pos):
        bPieceIndex = self.board[pos.x][pos.y]
        if bPieceIndex == -1:
            return False;
        if piece.index > 15:
            return bPieceIndex < 16;
        else:
            return bPieceIndex > 15;
    
    def actionSpace(self, index):
        piece = copy.deepcopy(self.pieces[index]);
        type = piece.__class__;
        moveableRange = piece.moveableRange;
        pos = self.realPos(piece);
        actionSpace = piece.transition();
        extraActionSpace = [];
        
        if type == Horse:
            if pos.y + 1 < 10 and self.board[pos.x][pos.y + 1] != -1:
                if piece.index < 16:
                    actionSpace = remove(actionSpace, Vec2d(1, 2));
                    actionSpace = remove(actionSpace, Vec2d(-1, 2));
                else:
                    actionSpace = remove(actionSpace, Vec2d(1, -2));
                    actionSpace = remove(actionSpace, Vec2d(-1, -2));
            if pos.y - 1 >= 0 and self.board[pos.x][pos.y - 1] != -1:
                if piece.index < 16:
                    actionSpace = remove(actionSpace, Vec2d(1, -2));
                    actionSpace = remove(actionSpace, Vec2d(-1, -2));
                else:
                    actionSpace = remove(actionSpace, Vec2d(1, 2));
                    actionSpace = remove(actionSpace, Vec2d(-1, 2));
            if pos.x + 1 < 9 and self.board[pos.x + 1][pos.y] != -1:
                if piece.index < 16:
                    actionSpace = remove(actionSpace, Vec2d(2, 1));
                    actionSpace = remove(actionSpace, Vec2d(2, -1));
                else:
                    actionSpace = remove(actionSpace, Vec2d(-2, 1));
                    actionSpace = remove(actionSpace, Vec2d(-2, -1));
            if pos.x - 1 >= 0 and self.board[pos.x - 1][pos.y] != -1:
                if piece.index < 16:
                    actionSpace = remove(actionSpace, Vec2d(-2, 1));
                    actionSpace = remove(actionSpace, Vec2d(-2, -1));
                else:
                    actionSpace = remove(actionSpace, Vec2d(2, 1));
                    actionSpace = remove(actionSpace, Vec2d(2, -1));
            
            poplist = [];
            
            for i in range(len(actionSpace)):
                newPiece = copy.deepcopy(piece);
                newPiece.move(actionSpace[i]);
                newPos = self.realPos(newPiece);
                if moveableRange.isInRange(newPiece.pos) == False or (self.board[newPos.x][newPos.y] != -1 and self.isOpponent(piece, newPos) == False):
                    poplist.append(i)
            poplist.sort();
            poplist.reverse();
            for popindex in poplist:
                actionSpace.pop(popindex)
            
            return actionSpace
        
        if type == Chariot or type == Cannon:
            for i in range(pos.x):
                if self.board[pos.x - i - 1][pos.y] == -1:
                    continue
                if self.isOpponent(piece, Vec2d(pos.x - i - 1, pos.y)):
                    if type == Chariot:
                        extraActionSpace.append(Vec2d(pos.x - i - 1, pos.y));
                if type == Cannon:
                    for j in range(i + 1, pos.x):
                        if self.board[pos.x - j - 1][pos.y] == -1:
                            continue
                        if self.isOpponent(piece, Vec2d(pos.x - j - 1, pos.y)):
                            extraActionSpace.append(Vec2d(pos.x - j - 1, pos.y));
                        break;
                if index < 16:
                    moveableRange.minVec.x = pos.x - i
                else:
                    moveableRange.maxVec.x = 8 - pos.x + i
                break;
            for i in range(pos.x, 8):
                if self.board[i + 1][pos.y] == -1:
                    continue
                if self.isOpponent(piece, Vec2d(i + 1, pos.y)):
                    if type == Chariot:
                        extraActionSpace.append(Vec2d(i + 1, pos.y));
                if type == Cannon:
                    for j in range(i + 1, 8):
                        if self.board[j + 1][pos.y] == -1:
                            continue
                        if self.isOpponent(piece, Vec2d(j + 1, pos.y)):
                            extraActionSpace.append(Vec2d(j + 1, pos.y));
                        break;
                if index < 16:
                    moveableRange.maxVec.x = i
                else:
                    moveableRange.minVec.x = 8 - i
                break
            for i in range(pos.y):
                if self.board[pos.x][pos.y - i - 1] == -1:
                    continue
                if self.isOpponent(piece, Vec2d(pos.x, pos.y - i - 1)):
                    if type == Chariot:
                        extraActionSpace.append(Vec2d(pos.x, pos.y - i - 1));
                if type == Cannon:
                    for j in range(i + 1, pos.y):
                        if self.board[pos.x][pos.y - j - 1] == -1:
                            continue
                        if self.isOpponent(piece, Vec2d(pos.x, pos.y - j - 1)):
                            extraActionSpace.append(Vec2d(pos.x, pos.y - j - 1));
                        break;
                if index < 16:
                    moveableRange.minVec.y = pos.y - i
                else:
                    moveableRange.maxVec.y = 9 - pos.y + i
                break
            for i in range(pos.y, 9):
                if self.board[pos.x][i + 1] == -1:
                    continue
                if self.isOpponent(piece, Vec2d(pos.x, i + 1)):
                    if type == Chariot:
                        extraActionSpace.append(Vec2d(pos.x, i + 1));
                if type == Cannon:
                    for j in range(i + 1, 9):
                        if self.board[pos.x][j + 1] == -1:
                            continue
                        if self.isOpponent(piece, Vec2d(pos.x, j + 1)):
                            extraActionSpace.append(Vec2d(pos.x, j + 1));
                        break;
                if index < 16:
                    moveableRange.maxVec.y = i
                else:
                    moveableRange.minVec.y = 9 - i
                break
        
        tmpRange = moveableRange
        
        if piece.index < 16:
            moveableRange.maxVec.y
            
        for i in range(len(extraActionSpace)):
            extraActionSpace[i] = self.logicPosIndex(index, extraActionSpace[i]) - self.pieces[index].pos;
        
        poplist = []
        
        for i in range(len(actionSpace)):
            newPiece = copy.deepcopy(piece);
            newPiece.move(actionSpace[i]);
            newPos = self.realPos(newPiece);
            if newPiece.__class__ == Cannon:
                print(newPiece.pos, newPos, moveableRange)
            if moveableRange.isInRange(newPiece.pos) == False or (self.board[newPos.x][newPos.y] != -1 and self.isOpponent(piece, newPos) == False):
                poplist.append(i)
        poplist.sort();
        poplist.reverse();
        
        for popindex in poplist:
            actionSpace.pop(popindex)
        
        return actionSpace + extraActionSpace
    
    def actionSpaces(self):
        actionSpaces = [];
        if self.turn == 'red':
            for i in range(16):
                if self.pieces[i].isAlive == False:
                    actionSpaces.append([]);
                else:
                    actionSpaces.append(self.actionSpace(i));
        else:
            for i in range(16, 32):
                if self.pieces[i].isAlive == False:
                    actionSpaces.append([]);
                else:
                    actionSpaces.append(self.actionSpace(i));
        return actionSpaces;
    
    def step(self, action):
        #action should be in the form of: [(integer)pieceIndex, (Vec2d)action]
        if self.turn == "black":
            pieceIndex = action[0] + 16;
            self.turn = "red"
            self.rounds += 1;
        else:
            pieceIndex = action[0];
            self.turn = "black"
        self.pieces[pieceIndex].move(action[1]);
        killed = None
        pos = self.realPos(self.pieces[pieceIndex])
        if self.isOpponent(self.pieces[pieceIndex], pos):
            oppIndex = self.board[pos.x][pos.y]
            self.pieces[oppIndex].isAlive = False;
            killed = self.pieces[oppIndex].__class__.__name__
        self.renderPieces()
        return killed
    
    def doGeneralsMeet(self):
        pos1 = self.realPos(self.pieces[0]);
        pos2 = self.realPos(self.pieces[16]);
        if pos1.x == pos2.x:
            for i in range(pos1.y + 1, pos2.y):
                if self.board[pos1.x][i] != -1:
                    return False;
            return True
        return False
    
    def __str__(self):
        self.renderPieces();
        ret = ""
        for i in range(10):
            for j in range(9):
                prt = "  "
                if self.board[j][9-i] == 0:
                    prt = "将"
                elif self.board[j][9-i] == 1 or self.board[j][9-i] == 2:
                    prt = "士"
                elif self.board[j][9-i] == 3 or self.board[j][9-i] == 4:
                    prt = "象"
                elif self.board[j][9-i] == 5 or self.board[j][9-i] == 6:
                    prt = "马"
                elif self.board[j][9-i] == 7 or self.board[j][9-i] == 8:
                    prt = "车"
                elif self.board[j][9-i] == 9 or self.board[j][9-i] == 10:
                    prt = "炮"
                elif self.board[j][9-i] >= 11 and self.board[j][9-i] <= 15:
                    prt = "兵"
                elif self.board[j][9-i] == 16:
                    prt = "将"
                elif self.board[j][9-i] == 17 or self.board[j][9-i] == 18:
                    prt = "士"
                elif self.board[j][9-i] == 19 or self.board[j][9-i] == 20:
                    prt = "象"
                elif self.board[j][9-i] == 21 or self.board[j][9-i] == 22:
                    prt = "马"
                elif self.board[j][9-i] == 23 or self.board[j][9-i] == 24:
                    prt = "车"
                elif self.board[j][9-i] == 25 or self.board[j][9-i] == 26:
                    prt = "炮"
                elif self.board[j][9-i] >= 27 and self.board[j][9-i] <= 31:
                    prt = "兵"
                ret += prt + " "
            if i != 9:
                ret += "\n"
        return ret
    
    def __repr__(self):
        return self.__str__()