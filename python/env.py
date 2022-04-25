from modules.board import Board

class XiangqiEnv():
    def __init__(self):
        self.board = Board();
    
    def actionSpace(self):
        return self.board.actionSpaces();
    
    def state(self):
        return self.board.board
    
    def step(self, action):
        killed = self.board.step(action);
        return killed, self.board.board, killed == 0 or killed == 16 or self.board.doGeneralsMeet()