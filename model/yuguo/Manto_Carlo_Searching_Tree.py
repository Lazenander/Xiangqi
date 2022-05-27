import os
import pickle
from math import log, sqrt
import numpy as np
import tqdm
from env import XiangqiEnv
from modules.vec2d import Vec2d
import copy


c=1
e=0.9


def load_model():
    global uct_b,uct_r,tree_s,path_s
    uct_b=None
    tree_s=None
    uct_r=None
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
        with open("./data/UCT_DATA_red_"+number+".model","rb+") as fin1:
            uct_r=pickle.load(fin1)
        with open("./data/Tree_structure_"+number+".model","rb+") as fin2:
            tree_s=pickle.load(fin2)
        with open("./data/UCT_DATA_black_"+number+".model","rb+") as fin3:
            uct_b=pickle.load(fin3)
    return uct_r,uct_b,tree_s

def totuple(states):
    state1=()
    for i in states:
        state1+=tuple(i)
    return state1

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
    def __init__(self,state):
        super().__init__()

        states=state.copy()
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
    def __init__(self,initial,turn):
        super().__init__(initial)
        if path_s==None:
            self.path=[totuple(initial)+(turn,)]
        else:
            self.path=path_s.copy()

    def random_move(self,actionSpace):
        self.actionspace=copy.deepcopy(actionSpace)
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
        #print(ucts,len(ucts))
        choose=list(next.keys())[ucts.index(max(ucts))]
        #print(ucts.index(max(ucts)))
        self.pieces_used=self.leaves(node)[choose][0]
        self.step=self.leaves(node)[choose][1]
        return [self.pieces_used,self.step]

        
    def backwards(self,win_or_lose,colour):
        #print(len(self.path))
        for i in self.path:
            if i[-1]==colour:
                self.update(i[:-1],win_or_lose)
            else:
                self.update(i[:-1],not win_or_lose)
        self.path=[initial+(chess.board.turn,)]
        return self.UCT
    def exploring_c(self,chess_state,on_or_off=False):
        global e
        if on_or_off==True:
            return len(self.leaves(totuple(chess_state)))<int(total_length(chess_state)) or float(np.random.randn())>e
        elif on_or_off=="train":
            return len(self.leaves(totuple(chess_state)))==0
        else:
            return len(self.leaves(totuple(chess_state)))<int(total_length(chess_state))
    def train(self,chess_state,on_or_off=False,):
        global c
        self.backup_path=[initial+(chess.board.turn,)]
        if self.exploring_c(chess_state,on_or_off):
            
            self.previous_state=chess.state().copy()
            self.move=self.random_move(chess.actionSpace())
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
            #print("Thinking")
            self.previous_state=totuple(chess.state())
            killed,self.state,self.signal=chess.step(self.choose_biggest(self.previous_state))
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
    chess=XiangqiEnv()
    initial=totuple(chess.state().copy())
    number=0
    uct_r,uct_b,tree_s=load_model()
    
    black=searching_tree(chess.state())
    red=searching_tree(chess.state())
    if not uct_b==None:
        black.UCT=uct_b
    if not uct_r==None:
        red.UCT=uct_r
    
    
    i=int(number)+1
    for turn in tqdm.tqdm(range(1,100001)):
        
        trees,path,signal,state=red.train(chess_state=chess.state())
        black.record(trees,path,signal,state)
        trees,path,signal,state=black.train(chess_state=chess.state())
        red.record(trees,path,signal,state)
    
        if turn%10000==0:
            with open("./data/UCT_DATA_red_"+str(i)+".model","wb") as fout:
                pickle.dump(red.UCT,fout)
            with open("./data/Tree_structure_"+str(i)+".model","wb") as fout2:
                pickle.dump(red.tree,fout2)
            with open("./data/UCT_DATA_black_"+str(i)+".model","wb") as fout3:
                pickle.dump(black.UCT,fout3)
            i+=1
        
        if turn%1000==0:
            print("\n",red.UCT[initial][1])
