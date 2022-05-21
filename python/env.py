from modules.board import Board

class XiangqiEnv():
    def __init__(self):
        self.board = Board();
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
        return killed, self.board.board, signal

    def translate(self):
        board=self.state().copy()
        trans=[]
        final_trans=""
        for i in range(9):
            tmp=[]
            for j in board[i]:
                tmp.append(j)
            trans.append(tmp*1)
        for i in range(10):
            line=""
            for j in range(9):
                if trans[j][9-i] == 0:
                    prt = "K"
                elif trans[j][9-i] == 1 or trans[j][9-i] == 2:
                    prt = "A"
                elif trans[j][9-i] == 3 or trans[j][9-i] == 4:
                    prt = "B"
                elif trans[j][9-i] == 5 or trans[j][9-i] == 6:
                    prt = "N"
                elif trans[j][9-i] == 7 or trans[j][9-i] == 8:
                    prt = "R"
                elif trans[j][9-i] == 9 or trans[j][9-i] == 10:
                    prt = "C"
                elif trans[j][9-i] >= 11 and trans[j][9-i] <= 15:
                    prt = "P"
                elif trans[j][9-i] == 16:
                    prt = "k"
                elif trans[j][9-i] == 17 or trans[j][9-i] == 18:
                    prt = "a"
                elif trans[j][9-i] == 19 or trans[j][9-i] == 20:
                    prt = "b"
                elif trans[j][9-i] == 21 or trans[j][9-i] == 22:
                    prt = "n"
                elif trans[j][9-i] == 23 or trans[j][9-i] == 24:
                    prt = "r"
                elif trans[j][9-i] == 25 or trans[j][9-i] == 26:
                    prt = "c"
                elif trans[j][9-i] >= 27 and trans[j][9-i] <= 31:
                    prt = "p"
                else:
                    prt=""
                line+=prt
                if prt=="":
                    if len(line)!=0:
                        if line[-1] in ["0","1","2","3","4","5","6","7","8","9"]:
                            line=line[:-1]+str(int(line[-1])+1)
                        else:
                            line+=str(1)
                    else:
                        line+=str(1)
            final_trans+=line+"/"
        final_trans=final_trans[0:-1]
        if self.board.turn=="red":
            final_trans=final_trans[0:-1]+" w"
            # +" - - "+str(0)+" "+str(self.board.rounds)
        elif self.board.turn=="black":
            final_trans=final_trans[0:-1]+" b"
            # +" - - "+str(0)+" "+str(self.board.rounds)
        return final_trans
        
    def __str__(self):
        board = self.board.__str__();
        return board;
    
    def __repr__(self):
        board = self.board.__repr__();
        return board;