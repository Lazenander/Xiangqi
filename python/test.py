from modules.vec2d import Vec2d
from env import XiangqiEnv

e = XiangqiEnv()
e.step([1, Vec2d(1, 1)])
e.step([1, Vec2d(1, 1)])
e.step([1, Vec2d(-1, -1)])
e.step([1, Vec2d(-1, -1)])

e.step([1, Vec2d(1, 1)])
e.step([1, Vec2d(1, 1)])
e.step([1, Vec2d(-1, -1)])
e.step([1, Vec2d(-1, -1)])

print(e.step([1, Vec2d(1, 1)]))
print(e.pastBoardsMap)