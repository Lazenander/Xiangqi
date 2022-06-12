import sys
from importlib import import_module
sys.path.append(sys.argv[1] + "/python")
sys.path.append(sys.argv[1] + "/models")

from env import XiangqiEnv

modelDir = input()
model = import_module(modelDir).Model

while model:
    pass