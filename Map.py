import numpy as np
import time
import math

class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Reigon:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.linkeds = []
        #중점, id로 사용
        self.id = ((start[0] + end[0])/2, (start[1] + end[1])/2)


class Map:
    def __init__(self, size):
        self.size = size
        #size 크기의 그리드 맵 생성(0: 빈공간, Entitiy: 개체, 1: 장애물)
        self.grid = [[0 for i in range(size[1])] for i in range(size[0])]
        self.walls = []
        self.reigons = {}
        self.vertical_lines = []
        self.horizontal_lines = []

    def getReigonID(self, start, end):
        return ((start[0] + end[0])/2, (start[1] + end[1])/2)
        
    def makeWall(self, start, end):
        for i in range(start[0], end[0]):
            for j in range(start[1], end[1]):
                self.grid[i][j] = 1
        self.walls.append(Wall(start, end))

    def makeregion(self):
        #장애물으로 인해 만들어진 가로세로 직선들
        vertical_lines = []
        horizontal_lines = []
        
        for i in range(len(self.walls)):
            #시점, 종점의 x좌표 -> 세로선
            vertical_lines.append(self.walls[i].start[0])
            vertical_lines.append(self.walls[i].end[0])
            #시점, 종점의 y좌표 -> 가로선
            horizontal_lines.append(self.walls[i].start[1])
            horizontal_lines.append(self.walls[i].end[1])

        #끝, 처음 추가 
        vertical_lines.append(0)
        vertical_lines.append(self.size[0])
        horizontal_lines.append(0)
        horizontal_lines.append(self.size[1])

        #중복 제거
        tv = set(vertical_lines)
        vertical_lines = list(tv)
        th = set(horizontal_lines)
        horizontal_lines = list(th)

        #정렬
        vertical_lines.sort()
        horizontal_lines.sort()

        self.vertical_lines = vertical_lines
        self.horizontal_lines = horizontal_lines


        print(vertical_lines)
        print(horizontal_lines)

        #구역 나누기
        for i in range(len(vertical_lines) - 1):
            for j in range(len(horizontal_lines) - 1):
                #현재 구역의 ID
                start = np.array([vertical_lines[i], horizontal_lines[j]])
                end = np.array([vertical_lines[i + 1], horizontal_lines[j + 1]])
                
                #구역 내가 장애물이면 구역 추가에서 제외
                if self.grid[start[0]][start[1]] != 1:
                    reg = Reigon(start, end)
                    self.reigons[reg.id] = reg
        
        #구역 연결하기
        for i in range(0, len(vertical_lines) - 1):
            for j in range(0, len(horizontal_lines) - 1):

                directionx = [-1, 0, 1, -1, 1, -1, 0, 1]
                directiony = [1, 1, 1, 0, 0, -1, -1, -1]
                
                #현재 구역의 ID
                start = np.array([vertical_lines[i], horizontal_lines[j]])
                end = np.array([vertical_lines[i + 1], horizontal_lines[j + 1]])

                #구역 내가 장애물이면 구역 추가에서 제외
                if self.grid[start[0]][start[1]] != 1:
                    for k in range(8):
                        #경계 오류 방지
                        if i + 2*directionx[k] < 0 or i + 2*directionx[k] >= len(vertical_lines):
                            continue
                        if i + 2*directiony[k] < 0 or j + 2*directiony[k] >= len(horizontal_lines):
                            continue
                
                        #연결할 구역의 ID
                        start1 = np.array([vertical_lines[i + directionx[k]], horizontal_lines[j + directiony[k]]])
                        end1 = np.array([vertical_lines[i + 2*directionx[k]], horizontal_lines[j + 2*directiony[k]]])
                        print(start1)
                        #연결할 구역이 장애물이 아니여야 함
                        if self.grid[math.floor((start1[0] + end1[0]) / 2)][math.floor((start1[1] + end1[1]) / 2)] != 1 and self.reigons in self.getReigonID(start1, end1):
                            reg = Reigon(start, end)
                            
                            if start[0] < end[0]:
                                reg1 = Reigon(start1, end1)
                            else:
                                reg1 = Reigon(end1, start1)


                            self.reigons[reg.id].linkeds.append(reg1.id)
                

                
                print(reg.id)
                                

                 
                


                

