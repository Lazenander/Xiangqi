from modules.board import Board

class XiangqiEnv():
    def __init__(self):
        self.board = Board();
        self.pastBoards = [];
        self.pastBoardsMap = {};
    
    def actionSpace(self):
        return self.board.actionSpaces();
    
    def state(self):
        return self.board.board
    
    def step(self, action):
        signal = False
        killed = self.board.step(action);
        if self.board.doGeneralsMeet():
            signal = "lose"
        if killed == 'General':
            signal = "win"
        fen = self.board.FEN()
        self.pastBoards.append(fen)
        round = self.board.rounds * 2
        if self.board.turn == "black":
            round += 1
        if fen not in self.pastBoardsMap.keys():
            self.pastBoardsMap[fen] = [round]
        else:
            self.pastBoardsMap[fen].append(round)
        if len(self.pastBoardsMap[fen]) >= 3 and self.pastBoardsMap[fen][-1] - self.pastBoardsMap[fen][-2] == self.pastBoardsMap[fen][-2] - self.pastBoardsMap[fen][-3]:
            diff = self.pastBoardsMap[fen][-1] - self.pastBoardsMap[fen][-2]
            print(diff, self.pastBoards[-diff:][0], self.pastBoards[-2*diff:-diff][0], self.pastBoards[-3*diff:-2*diff][0])
            if len(self.pastBoards) >= 3 * diff and self.pastBoards[-diff:] == self.pastBoards[-2*diff:-diff] and self.pastBoards[-2*diff:-diff] == self.pastBoards[-3*diff:-2*diff]:
                return killed, self.board.board, "lose"
        return killed, self.board.board, signal
        
    def __str__(self):
        board = self.board.__str__();
        return board;
    
    def __repr__(self):
        board = self.board.__repr__();
        return board;