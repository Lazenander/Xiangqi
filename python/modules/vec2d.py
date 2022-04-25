class Vec2d:
    def __init__(self, x = 0, y = 0):
        self.x = x;
        self.y = y;
        
    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y);
    
    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y);

class Range2d:
    def __init__(self, minVec = Vec2d(), maxVec = Vec2d()):
        self.minVec = minVec;
        self.maxVec = maxVec;
    
    def isInRange(self, pos):
        if pos.x < self.minVec.x:
            return False
        if pos.y < self.minVec.y:
            return False
        if pos.x > self.maxVec.x:
            return False
        if pos.y > self.maxVec.y:
            return False
        return True
    
    def size(self):
        return Vec2d(self.maxVec.x - self.minVec.x + 1, self.maxVec.y - self.minVec.y + 1);