import json
import sys
from importlib import import_module
sys.path.append(sys.argv[1] + "/python")
sys.path.append(sys.argv[1] + "/models")

from env import XiangqiEnv
from modules.vec2d import Vec2d

def Vec2ds2List(vec2dlst):
    lst = []
    for i in range(len(vec2dlst)):
        lst.append([])
        for j in range(len(vec2dlst[i])):
            lst[i].append([vec2dlst[i][j].x, vec2dlst[i][j].y])
    
    return lst

AIModel = import_module(sys.argv[2]).Model

e = XiangqiEnv()
model = AIModel()

while True:
    print(json.dumps({"type": "board", "state": e.state(), "actionSpace": Vec2ds2List(e.actionSpace())}))
    
    userAction = [0, Vec2d()]
    userAction[0], userAction[1].x, userAction[1].y = [int(x) for x in input().split(' ')]
    
    _, _, signal = e.step(userAction)
    if signal:
        print(json.dumps({"type": "signal", "player": "user", "value": signal}))
    
    aiAction = model.action(e.state(), e.actionSpace())
    _, _, signal = e.step(userAction)
    if signal:
        print(json.dumps({"type": "signal", "player": "ai", "value": signal}))