from modules.Manto_Carlo_Searching_Tree import load_model,searching_tree,totuple
import os
import sys
sys.path.append(os.getcwd() + "/../python")
from env import XiangqiEnv

class Model(searching_tree):
    def __init__(self,initial_state,turn):
        uct_r,uct_b,tree_s=load_model()
        super().__init__(initial_state,turn)
        self.UCT=uct_r
        self.tree=tree_s

    def action(self,state,actionSpace):
        if self.exploring_c(state,"train"):
            self.move=self.random_move(actionSpace)
        else:
            self.move=self.choose_biggest(totuple(state))
        return self.move
