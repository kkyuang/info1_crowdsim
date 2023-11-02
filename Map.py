from Entity import Entity
import numpy as np
import time

class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Map:
    def __init__(self, size):
        self.size = size
        #size 크기의 그리드 맵 생성(0: 빈공간, Entitiy: 개체, 1: 장애물)
        self.grid = [[0 for i in range(size[1])] for i in range(size[0])]
        self.walls = []
        
    def makeWall(self, start, end):
        for i in range(start[0], end[0]):
            for j in range(start[1], end[1]):
                self.grid[i][j] = 1
        self.walls.append(Wall(start, end))
