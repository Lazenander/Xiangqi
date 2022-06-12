import random
import sys

class Model:
    def action(state, actionSpace):
        cnt = 0
        for action in actionSpace:
            if action != []:
                cnt += 1
        index = random.randint(0, cnt - 1);
        cnt = 0
        for i in len(actionSpace):
            if actionSpace[i] == []:
                continue
            if cnt == index:
                action = actionSpace[i][random.randint(0, len(actionSpace[i]) - 1)]
                return index, action.x, action.y