import modules.cloudAPI as cloudAPI
from modules.board import Board

class XiangqiEnv():
    def __init__(self):
        self.board = Board()
        self.pastboards = []
        self.pastmoves = []
        self.lastrule = None
        self.turn = "w"
    
    def reset(self):
        self.board = Board()
        self.pastboards = []
        self.pastmoves = []
        self.lastrule = None
        self.turn = "w"
    
    def state(self):
        return self.board.board, self.turn
    
    def actionSpace(self):
        moves = cloudAPI.queryall(self.board.FEN() + " " + self.turn)
        if moves == "invalid board":
            return "Failed"
        if moves == "unknown":
            return "Unknown"
        if moves == "checkmate" or moves == "stalemate":
            return "Lose"
        return [moves[move]["move"] for move in moves]
    
    def step(self, move):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"
        tmpPiece = self.board.move(move)
        self.pastmoves.append(move)
        if len(self.pastboards) < 5:
            self.pastboards.append(self.board.FEN() + " " + self.turn)
            return tmpPiece, "None"
        rule = cloudAPI.queryrule(self.pastboards[-4], self.pastmoves[-4:])
        self.pastboards.append(self.board.FEN() + " " + self.turn)
        if rule == "invalid board" or rule == "invalid movelist":
            return tmpPiece, "Failed"
        if rule == "checkmate" or rule == "stalemate":
            return tmpPiece, "Lose"
        if self.lastrule == None:
            self.lastrule = rule
            return tmpPiece, "None"
        if self.lastrule[move].rule == "none":
            self.lastrule = rule
            return tmpPiece, "None"
        if self.lastrule[move].rule == "ban":
            self.lastrule = rule
            return tmpPiece, "Ban"
        if self.lastrule[move].rule == "draw":
            self.lastrule = rule
            return tmpPiece, "Draw"
    
    def __str__(self):
        retstr = self.turn + "'s Turn\n"
        retstr += str(self.board)
        return retstr
    
    def __repr__(self):
        return self.__str__()