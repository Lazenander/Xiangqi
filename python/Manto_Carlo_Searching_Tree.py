import pickle
from math import sqrt,log
import numpy as np
from env import XiangqiEnv
from modules.vec2d import Vec2d
from functools import reduce
import tqdm
c=1
chess=XiangqiEnv()
e=0.9
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

    def calc(self,Q,Ni,N,c):
        possibility=float(Q)/float(N)+c*sqrt(log(Ni)/N)
        return possibility
    def update(self,node,win_or_lose):
        self.UCT[node]=[self.UCT[node][0]+int(win_or_lose),self.UCT[node][1]+1]
        return self.UCT
    def uct(self,node):
        self.Ni=self.UCT[node][1]
        return self.calc(self.UCT[node][0],self.Ni,self.UCT[node][1],c)
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
    def exploring_c(self,on_or_off):
        global e
        if on_or_off:
            return len(self.leaves(totuple(chess.state())))<isNotEmpty(chess.actionSpace()) or float(np.random.randn())>e
        else:
            return len(self.leaves(totuple(chess.state())))<isNotEmpty(chess.actionSpace())
    def train(self,on_or_off=True):
        global c
        self.backup_path=[initial]
        if self.exploring_c(on_or_off):
            
            self.previous_state=chess.state().copy()
            self.move=self.random_move()
            kill,state,self.signal=chess.step(self.move)
            self.path.append(totuple(state))
            if self.isExist(totuple(state)):
                pass
            else:
                self.add_leaves(totuple(self.previous_state),totuple(state),self.move[0],self.move[1])
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
            if self.signal=="win":
                self.backwards(True)
                chess.board.reset()
            elif self.signal=="lose":
                self.backwards(False)
                chess.board.reset()
        return self.tree,self.backup_path,self.signal,state
    def record(self,tree,path,signal,state):
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
    last_epoch=1
    for turn in tqdm.tqdm(range(100000)):
        trees,path,signal,state=red.train()
        black.record(trees,path,signal,state)
        trees,path,signal,state=black.train()
        red.record(trees,path,signal,state)
       # if turn%500==0:
           # print(red.UCT[initial],"steps:",turn," ","length:",len(red.UCT)," ","Increase",(len(red.UCT)-last_epoch)," ","Increase percentage:",((len(red.UCT)-last_epoch)/last_epoch)*100,"%","\n")
           # last_epoch=len(red.UCT)
    
    
    with open("UCT_DATA.txt","wb") as fout:
        pickle.dump(red.UCT,fout)

    with open("Tree_structure.txt","wb") as fout2:
        pickle.dump(red.tree,fout2)