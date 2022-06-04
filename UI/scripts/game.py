import sys
from importlib import import_module
sys.path.append("../../python")
sys.path.append("../../models")

from env import XiangqiEnv

modelDir = input()
model = import_module(modelDir).Model

print(model)