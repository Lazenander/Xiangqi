from math import sqrt,log
import numpy as np
from pyrsistent import b
from env import XiangqiEnv
from modules.vec2d import Vec2d
Ni=0
c=2
chess=XiangqiEnv()

np.random.seed(123)
def totuple(states):
    state=()
    for i in states:
        state+=tuple(i)
    return state
initial=totuple(chess.state().copy())
def isNotEmpty(list):
    num=0
    for i in list:
        if i!=None:
            num+=1
    return num
class tree:
    def __init__(self):
        self.tree={}
    def add_leaves(self,parent,son,pieces,moves):
        temp=self.tree[parent]
        temp[son]=[pieces,moves]
        if son not in self.tree:
            self.tree[son]={}
        return self.tree
    def isExist(self,tar):
        return tar in self.tree
    def leaves(self,tar):
        if tar not in self.tree:
            self.tree[tar]={}
        return self.tree[tar]
    def structure(self):
        print(self.tree)
        return self.tree
    
class UCT(tree):
    def __init__(self):
        super().__init__()
        states=chess.state().copy()
        state=totuple(states)
        self.UCT={state:[0,0]}
        self.tree={state:{}}
    def add_leaves(self,parent,son,pieces,moves):
        temp=self.tree[parent]
        temp[son]=[pieces,moves]
        self.tree[son]={}
        self.UCT[son]=[0,1]
        return self.tree

    def calc(self,Q,N,Ni,c):
        possibility=float(Q)/float(N)+c*sqrt(log(N,10)/Ni)
        return possibility
    def update(self,node,win_or_lose):
        self.UCT[node]=[self.UCT[node][0]+int(win_or_lose),self.UCT[node][1]+1]
        return self.UCT
    def uct(self,node):
        return self.calc(self.UCT[node][0],self.UCT[node][1],Ni,c)
    def data(self):
        return self.UCT

class searching_tree(UCT):
    def __init__(self):
        super().__init__()
        self.path=[initial]
    def random_move(self):
        self.actionspace=chess.actionSpace()
        self.actions=[]
        while self.actions==[]:
            self.pieces=np.random.randint(len(self.actionspace))
            self.actions=self.actionspace[self.pieces]
        self.action=self.actions[np.random.randint(len(self.actions))]

        return [self.pieces,self.action]
 
    def choose_biggest(self,node):
        next=self.leaves(node)
        ucts=[]
        for k in next.keys():
            ucts.append(self.uct(k))
        choose=list(next.keys())[ucts.index(max(ucts))]
        pieces=self.leaves(node)[choose][0]
        step=self.leaves(node)[choose][1]
        return [pieces,step]

        
    def backwards(self,win_or_lose):
        for i in self.path:
            self.update(i,win_or_lose)
        self.path=[initial]
        return self.UCT
    def train(self):
        global Ni,c
        self.backup_path=[initial]
        if len(self.leaves(totuple(chess.state())))<isNotEmpty(chess.actionSpace()):
            self.previous_state=chess.state().copy()
            self.move=self.random_move()
            kill,state,self.signal=chess.step(self.move)
            self.path.append(totuple(state))
            if self.isExist(totuple(state)):
                pass
            else:
                self.add_leaves(totuple(self.previous_state),totuple(state),self.move[0],self.move[1])
            Ni+=1
            if self.signal=="win":
                self.backwards(True)
                chess.board.reset()

            elif self.signal=="lose":
                self.backwards(False)
                chess.board.reset()
        else:
            self.previous_state=totuple(chess.state())
            kill,state,self.signal=chess.step(self.choose_biggest(self.previous_state))
            self.path.append(totuple(state))
            self.backup_path=self.path.copy()
            Ni+=1
            if self.signal=="win":
                self.backwards(True)
                chess.board.reset()
            elif self.signal=="lose":
                self.backwards(False)
                chess.board.reset()
        return self.previous_state,self.tree,self.backup_path,self.signal,state
    def record(self,UCT,tree,path,signal,state):
        self.tree=tree
        self.path=path
        self.UCT[totuple(state)]=[0,1]
        if signal=="win":
            self.backwards(False)
            chess.board.reset()
        elif signal=="lose":
            self.backwards(True)
            chess.board.reset()



black=searching_tree()
red=searching_tree()
if __name__=="__main__":
    for turn in range(100000000):
        uct,trees,path,signal,state=red.train()
        black.record(uct,trees,path,signal,state)
        uct,trees,path,signal,state=black.train()
        red.record(uct,trees,path,signal,state)
        if turn%100==0:
            print(red.UCT[initial])
