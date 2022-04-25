from vec2d import Vec2d, Range2d

class Piece:
    def __init__(self, index, pos):
        # What index stands for:
        # 0: red general
        # 1: red guardian1
        # 2: red guardian2
        # 3: red elephant1
        # 4: red elephant2
        # 5: red horse1
        # 6: red horse2
        # 7: red chariot1
        # 8: red chariot2
        # 9: red cannon1
        # 10: red cannon2
        # 11: red soldier1
        # 12: red soldier2
        # 13: red soldier3
        # 14: red soldier4
        # 15: red soldier5
        # 16: black general
        # 17: black guardian1
        # 18: black guardian2
        # 19: black elephant1
        # 20: black elephant2
        # 21: black horse1
        # 22: black horse2
        # 23: black chariot1
        # 24: black chariot2
        # 25: black cannon1
        # 26: black cannon2
        # 27: black soldier1
        # 28: black soldier2
        # 29: black soldier3
        # 30: black soldier4
        # 31: black soldier5
        self.index = index
        self.pos = pos
        self.moveableRange = Range2d(Vec2d(3, 0), Vec2d(5, 2))
        self.isAlive = True
    
    def move(self, transition):
        self.pos = self.pos + transition;
    
    def transition(self):
        return [];

class General(Piece):
    def __init__(self,index, pos):
        super(General, self).__init__(index, pos)
        self.moveableRange = Range2d(Vec2d(3, 0), Vec2d(5, 2))
    
    def transition(self):
        return [Vec2d(1, 0), Vec2d(-1, 0), Vec2d(0, 1), Vec2d(0, -1)]

class Guardian(Piece):
    def __init__(self, index, pos):
        super(Guardian, self).__init__(index, pos);
        self.moveableRange = Range2d(Vec2d(3, 0), Vec2d(5, 2))
    
    def transition(self):
        return [Vec2d(1, 1), Vec2d(-1, 1), Vec2d(-1, 1), Vec2d(-1, -1)]

class Elephant(Piece):
    def __init__(self, index, pos):
        super(Elephant, self).__init__(index, pos);
        self.moveableRange = Range2d(Vec2d(0, 0), Vec2d(8, 4))
    
    def transition(self):
        return [Vec2d(2, 2), Vec2d(-2, 2), Vec2d(-2, 2), Vec2d(-2, -2)]

class Horse(Piece):
    def __init__(self, index, pos):
        super(Horse, self).__init__(index, pos);
        self.moveableRange = Range2d(Vec2d(0, 0), Vec2d(8, 9))
    
    def transition(self):
        return [Vec2d(1, 2), Vec2d(-1, 2), Vec2d(1, -2), Vec2d(-1, -2),Vec2d(2, 1), Vec2d(-2, 1), Vec2d(2, -1), Vec2d(-2, -1)]

class Chariot(Piece):
    def __init__(self, index, pos):
        super(Chariot, self).__init__(index, pos);
        self.moveableRange = Range2d(Vec2d(0, 0), Vec2d(8, 9))
    
    def transition(self):
        return [Vec2d(i, 0) for i in range(9)]+[Vec2d(-i, 0) for i in range(9)]+[Vec2d(0, i) for i in range(10)]+[Vec2d(0, -i) for i in range(10)]

class Cannon(Piece):
    def __init__(self, index, pos):
        super(Cannon, self).__init__(index, pos);
        self.moveableRange = Range2d(Vec2d(0, 0), Vec2d(8, 9))
    
    def transition(self):
        return [Vec2d(i, 0) for i in range(9)]+[Vec2d(-i, 0) for i in range(9)]+[Vec2d(0, i) for i in range(10)]+[Vec2d(0, -i) for i in range(10)]

class Soldier(Piece):
    def __init__(self, index, pos):
        super(Soldier, self).__init__(index, pos);
        self.moveableRange = Range2d(Vec2d(0, 0), Vec2d(8, 9))
    
    def transition(self):
        if self.pos.y <= 4:
            return [Vec2d(0, 1)]
        else:
            return [Vec2d(0, 1), Vec2d(1, 0), Vec2d(-1, 0)]