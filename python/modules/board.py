import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)));

from pieces import General, Guardian, Elephant, Horse, Chariot, Cannon, Soldier
from vec2d import Vec2d, Range2d
import copy

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
        print(self.board)
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
    
    def renderPieces(self):
        for piece in self.pieces:
            pos = self.realPos(piece)
            print(pos.x, pos.y)
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
        piece = self.pieces[index];
        type = piece.__class__.__name__;
        range = piece.moveableRange;
        pos = self.realPos(piece);
        actionSpace = piece.transition();
        extraActionSpace = [];
        
        if type == Horse:
            if pos.y + 1 < 10 and self.board[pos.x][pos.y + 1] != -1:
                if piece.index < 16:
                    actionSpace.remove(Vec2d(1, 2));
                    actionSpace.remove(Vec2d(-1, 2));
                else:
                    actionSpace.remove(Vec2d(1, -2));
                    actionSpace.remove(Vec2d(-1, -2));
            if pos.y + 1 < 10 and self.board[pos.x][pos.y - 1] != -1:
                if piece.index < 16:
                    actionSpace.remove(Vec2d(1, -2));
                    actionSpace.remove(Vec2d(-1, -2));
                else:
                    actionSpace.remove(Vec2d(1, 2));
                    actionSpace.remove(Vec2d(-1, 2));
            if pos.y + 1 < 10 and self.board[pos.x + 1][pos.y] != -1:
                if piece.index < 16:
                    actionSpace.remove(Vec2d(2, 1));
                    actionSpace.remove(Vec2d(2, -1));
                else:
                    actionSpace.remove(Vec2d(-2, 1));
                    actionSpace.remove(Vec2d(-2, -1));
            if pos.y + 1 < 10 and self.board[pos.x - 1][pos.y] != -1:
                if piece.index < 16:
                    actionSpace.remove(Vec2d(-2, 1));
                    actionSpace.remove(Vec2d(-2, -1));
                else:
                    actionSpace.remove(Vec2d(2, 1));
                    actionSpace.remove(Vec2d(2, -1));
                
            for i in range(len(actionSpace)):
                newPiece = copy.deepcopy(piece);
                newPiece.move(actionSpace[i]);
                newPos = self.realPos(newPiece);
                if range.isInRange() == False or (self.board[newPos.x][newPos.y] != -1 and self.isOpponent(piece, newPos) == False):
                    actionSpace.pop(i);
            
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
                range.minVec.x = pos.x - i
                break;
            for i in range(pos.x, 9):
                if self.board[i + 1][pos.y] == -1:
                    continue
                if self.isOpponent(piece, Vec2d(i + 1, pos.y)):
                    if type == Chariot:
                        extraActionSpace.append(Vec2d(i + 1, pos.y));
                if type == Cannon:
                    for j in range(i + 1, 9):
                        if self.board[j + 1][pos.y] == -1:
                            continue
                        if self.isOpponent(piece, Vec2d(j + 1, pos.y)):
                            extraActionSpace.append(Vec2d(j + 1, pos.y));
                        break;
                range.maxVec.x = i
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
                range.minVec.y = pos.y - i
                break
            for i in range(pos.y, 10):
                if self.board[pos.x][i + 1] == -1:
                    continue
                if self.isOpponent(piece, Vec2d(pos.x, i + 1)):
                    if type == Chariot:
                        extraActionSpace.append(Vec2d(pos.x, i + 1));
                if type == Cannon:
                    for j in range(i + 1, 10):
                        if self.board[pos.x][j + 1] == -1:
                            continue
                        if self.isOpponent(piece, Vec2d(pos.x, j + 1)):
                            extraActionSpace.append(Vec2d(pos.x, j + 1));
                        break;
                range.maxVec.y = i
                break
            
        print(extraActionSpace)
            
        for i in range(len(extraActionSpace)):
            extraActionSpace[i] = self.logicPos(extraActionSpace[i]);
        
        for i in range(len(actionSpace)):
            newPiece = copy.deepcopy(piece);
            newPiece.move(actionSpace[i]);
            newPos = self.realPos(newPiece);
            if range.isInRange() == False or (self.board[newPos.x][newPos.y] != -1 and self.isOpponent(piece, newPos) == False):
                actionSpace.pop(i);
        
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
            piece = self.pieces[action[0] + 16];
            self.turn = "red"
            self.round += 1;
        else:
            piece = self.pieces[action[0]];
            self.turn = "black"
        piece.move(action[1]);
        killed = None
        pos = self.realPos(piece)
        if self.isOpponent(piece, pos):
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