import os
import pickle
from functools import reduce
from math import log, sqrt

import numpy as np

from env import XiangqiEnv
from modules.vec2d import Vec2d

uct_b=None
uct_r=None
tree_s=None
path_s=None
number="0"
if not os.path.exists("./data"):
    os.mkdir("./data")
elif len(os.listdir("./data"))==0:
    pass
else:
    filename=os.listdir("./data")
    number=""
    name=[]
    for k in filename:
        number=""
        for i in k:
            if i in ["0","1","2","3","4","5","6","7","8","9"]:
                number+=i
        name.append(int(number))
    number=str(max(name))
    print(number)
    with open("./data/UCT_DATA_red_"+number+".txt","rb+") as fin1:
        uct_r=pickle.load(fin1)
    with open("./data/Tree_structure_"+number+".txt","rb+") as fin2:
        tree_s=pickle.load(fin2)
    with open("./data/UCT_DATA_black_"+number+".txt","rb+") as fin3:
        uct_b=pickle.load(fin3)

c=1
chess=XiangqiEnv()
e=0.9
def totuple(states):
    state1=()
    for i in states:
        state1+=tuple(i)
    return state1
initial=totuple(chess.state().copy())
def isNotEmpty(list):
    num=0
    for i in list:
        if i!=None:
            num+=1
    return num
def total_length(list):
    n=0
    for i in list:
        n+=len(i)
    return n
class tree:
    def __init__(self):
        if tree_s==None:
            self.tree={}
        else:
            self.tree=tree_s
    def add_leaves(self,parent,son,pieces,moves):
        temp=self.tree[parent]
        temp[son]=[pieces,moves]
        if son not in self.tree:
            self.tree[son]={}
        return self.tree
    def isExist(self,tar):
        return tar in self.tree
    def leaves(self,tar):
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
        if tree_s==None:
            self.tree={state:{}}
    def add_leaves(self,parent,son,pieces,moves):
        temp=self.tree[parent]
        temp[son]=[pieces,moves]
        if son not in self.tree:
            self.tree[son]={}
            self.UCT[son]=[0,1]

        return self.tree

    def calc(self,Q,Ni,N,c):
        possibility=float(Q)/float(N)+float(c)*sqrt(log(float(Ni))/float(N))
        return possibility
    def update(self,node,win_or_lose):
        if win_or_lose:
            self.UCT[node]=[self.UCT[node][0]+int(win_or_lose),self.UCT[node][1]+1]
        else:
            self.UCT[node]=[self.UCT[node][0]+int(-2),self.UCT[node][1]+1]
        return self.UCT
    def uct(self,node,last_node):
        self.Ni=self.UCT[last_node][1]
        return self.calc(self.UCT[node][0],self.Ni,self.UCT[node][1],c)
    def data(self):
        return self.UCT

class searching_tree(UCT):
    def __init__(self):
        super().__init__()
        if path_s==None:
            self.path=[initial+(chess.board.turn,)]
        else:
            self.path=path_s.copy()
    def random_move(self):
        self.actionspace=chess.actionSpace().copy()
        self.actions=[]
        while self.actions==[]:
            self.pieces=np.random.randint(len(self.actionspace))
            self.actions=self.actionspace[self.pieces]      #Use pop()
        self.action=self.actions[np.random.randint(len(self.actions))]

        return [self.pieces,self.action]

        
        

    def choose_biggest(self,node):
        next=self.leaves(node)
        ucts=[]
        for k in next:
            ucts.append(self.uct(k,node))
        print(ucts)
        choose=list(next.keys())[ucts.index(max(ucts))]
        #print(ucts.index(max(ucts)))
        pieces=self.leaves(node)[choose][0]
        step=self.leaves(node)[choose][1]
        return [pieces,step]

        
    def backwards(self,win_or_lose,colour):
        #print(len(self.path))
        for i in self.path:
            if i[-1]==colour:
                self.update(i[:-1],win_or_lose)
            else:
                self.update(i[:-1],not win_or_lose)
        self.path=[initial+(chess.board.turn,)]
        return self.UCT
    def exploring_c(self,on_or_off=False):
        global e
        if on_or_off==True:
            return len(self.leaves(totuple(chess.state())))<int(total_length(chess.actionSpace())) or float(np.random.randn())>e
        elif on_or_off=="train":
            return len(self.leaves(totuple(chess.state())))==0
        else:
            return len(self.leaves(totuple(chess.state())))<int(total_length(chess.actionSpace()))
    def train(self,on_or_off=False):
        global c
        self.backup_path=[initial+(chess.board.turn,)]
        if self.exploring_c(on_or_off):
            
            self.previous_state=chess.state().copy()
            self.move=self.random_move()
            kill,self.state,self.signal=chess.step(self.move)
            self.path.append(totuple(self.state)+(chess.board.turn,))
            self.paths=self.path.copy()
            #print(len(self.path))
            if self.isExist(totuple(self.state)):
                pass
            else:
                self.add_leaves(totuple(self.previous_state),totuple(self.state),self.move[0],self.move[1])
            if self.signal=="win":
                self.backwards(True,chess.board.turn)
                chess.board.reset()

            elif self.signal=="lose":
                self.backwards(False,chess.board.turn)
                chess.board.reset()
        else:
            print("Thinking")
            self.previous_state=totuple(chess.state())
            killed,self.state,self.signal=chess.step(self.choose_biggest(self.previous_state))
            print(killed)
            self.path.append(totuple(self.state)+(chess.board.turn,))
            self.paths=self.path.copy()
            if self.signal=="win":
                self.backwards(True,chess.board.turn)
                chess.board.reset()
            elif self.signal=="lose":
                self.backwards(False,chess.board.turn)
                chess.board.reset()
        return self.tree,self.paths,self.signal,self.state.copy()
    def record(self,tree,paths,signal,state):
        self.tree=tree.copy()
        self.path=paths.copy()
        self.UCT[totuple(state)]=[0,1]
        if signal=="win":
            self.backwards(False,chess.board.turn)
            chess.board.reset()
        elif signal=="lose":
            self.backwards(True,chess.board.turn)
            chess.board.reset()



if __name__=="__main__":
    
    black=searching_tree()
    red=searching_tree()
    if not uct_b==None:
        black.UCT=uct_b
    if not uct_r==None:
        red.UCT=uct_r
    
    i=int(number)+1
    for turn in range(1,1000001):
        trees,path,signal,state=red.train()
        black.record(trees,path,signal,state)
        trees,path,signal,state=black.train()
        red.record(trees,path,signal,state)
        if turn%10000==0:
            with open("./data/UCT_DATA_red_"+str(i)+".txt","wb") as fout:
                pickle.dump(red.UCT,fout)
            with open("./data/Tree_structure_"+str(i)+".txt","wb") as fout2:
                pickle.dump(red.tree,fout2)
            with open("./data/UCT_DATA_black_"+str(i)+".txt","wb") as fout3:
                pickle.dump(black.UCT,fout3)
            i+=1
