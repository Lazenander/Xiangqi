from modules.board import Board

class XiangqiEnv():
    def __init__(self):
        self.board = Board();
    
    def actionSpace(self):
        return self.board.actionSpaces();
    
    def state(self):
        return self.board.board
    
    def reset(self):
        return self.board.reset()
    
    def step(self, action):
        signal = False
        killed = self.board.step(action);
        if self.board.doGeneralsMeet():
            signal = "lose"
        if killed == 'General':
            signal = "win"
        return killed, self.board.board, signal

    def __str__(self):
        board = self.board.__str__();
        return board;
    
    def __repr__(self):
        board = self.board.__repr__();
        return board;