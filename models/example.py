import random
import os
import sys
sys.path.append(os.getcwd() + "/../python")
from modules.vec2d import Vec2d

class Model:
    def action(self, state, actionSpace):
        cnt = 0
        for action in actionSpace:
            if action != []:
                cnt += 1
        index = random.randint(0, cnt - 1);
        cnt = 0
        for action in actionSpace:
            if action == []:
                continue
            if cnt == index:
                action = action[random.randint(0, len(action) - 1)]
                return [index, action]
            cnt += 1