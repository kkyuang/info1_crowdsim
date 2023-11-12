import numpy as np
import time
import math

class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Shelter:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.id = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)

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
        #장애물의 (시작, 끝) 튜플 배열
        self.walls = []
        #대피소(출구)의
        self.shelters = []
        #구역들
        self.reigons = {}
        #구역에 따른 인구수
        self.reigonsPopulation = {}
        #세로줄
        self.vertical_lines = []
        #가로줄
        self.horizontal_lines = []

        #구역에 따른 대피소 지도
        self.shelterAssignMap = {}
        self.shelterTempArr = []


    def getReigonID(self, start, end):
        return ((start[0] + end[0])/2, (start[1] + end[1])/2)

    def regionDensity(self, regionID):
        popul = len(self.reigonsPopulation[regionID])
        area = (self.reigons[regionID].end[0] - self.reigons[regionID].start[0])*(self.reigons[regionID].end[1] - self.reigons[regionID].start[1])
        return (popul / area)
    
    def addEntityReigon(self, astar, entities):
        for i in self.reigons.keys():
            self.reigonsPopulation[i] = []

        for i in entities:
            if astar.getReigon(i.position) in self.reigons.keys():
                self.reigonsPopulation[astar.getReigon(i.position)].append(i)
        
    def makeWall(self, start, end):
        for i in range(start[0], end[0]):
            for j in range(start[1], end[1]):
                self.grid[i][j] = 1
        self.walls.append(Wall(start, end))

    def makeShelter(self, start, end):
        for i in range(start[0], end[0]):
            for j in range(start[1], end[1]):
                self.grid[i][j] = 2
        self.shelters.append(Shelter(start, end))


    #현재 위치한 구역
    def getReigon(self, position):
        myReigonStart = np.array([0, 0])
        myReigonEnd = np.array([0, 0])
        for i in range(len(self.vertical_lines)-1):
            if self.vertical_lines[i] <= position[0] and position[0] < self.vertical_lines[i + 1]:
                myReigonStart[0] = self.vertical_lines[i]
                myReigonEnd[0] = self.vertical_lines[i+1]

        for i in range(len(self.horizontal_lines)-1):
            if self.horizontal_lines[i] <= position[1] and position[1] < self.horizontal_lines[i + 1]:
                myReigonStart[1] = self.horizontal_lines[i]
                myReigonEnd[1] = self.horizontal_lines[i+1]

        return self.getReigonID(myReigonStart, myReigonEnd)
    
    #구역에 따른 대피소 분배
    def setShelterDist(self):
        self.shelterTempArr.append([(self.getReigon(i.id), i.id)  for i in (self.shelters)])
        print(self.shelterTempArr[-1])
        while len(self.shelterTempArr[-1]) != 0:
            i = len(self.shelterTempArr)
            self.shelterTempArr.append([])
            for j in self.shelterTempArr[i - 1]:
                self.shelterAssignMap[j[0]] = j[1]
                for k in self.reigons[j[0]].linkeds:
                    if not (k in self.shelterAssignMap.keys()):
                        self.shelterTempArr[i].append((k, j[1]))
                        self.shelterAssignMap[k] = j[1]
                    else:
                        pass
        

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

        for i in range(len(self.shelters)):
            #시점, 종점의 x좌표 -> 세로선
            vertical_lines.append(self.shelters[i].start[0])
            vertical_lines.append(self.shelters[i].end[0])
            #시점, 종점의 y좌표 -> 가로선
            horizontal_lines.append(self.shelters[i].start[1])
            horizontal_lines.append(self.shelters[i].end[1])

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


        #구역 나누기
        for i in range(len(vertical_lines) - 1):
            for j in range(len(horizontal_lines) - 1):
                #현재 구역의 ID
                start = np.array([vertical_lines[i], horizontal_lines[j]])
                end = np.array([vertical_lines[i + 1], horizontal_lines[j + 1]])
                
                #구역 내가 장애물이면 구역 추가에서 제외
                if self.grid[math.floor((start[0] + end[0]) / 2)][math.floor((start[1] + end[1]) / 2)] != 1:
                    reg = Reigon(start, end)
                    self.reigons[reg.id] = reg
        
        #구역 연결하기
        for i in range(0, len(vertical_lines) - 1):
            for j in range(0, len(horizontal_lines) - 1):

                #directionx = [-1, 0, 1, -1, 1, -1, 0, 1]
                #directiony = [1, 1, 1, 0, 0, -1, -1, -1]
                directionx = [1, 0, 0, -1]
                directiony = [0, -1, 1, 0]
                
                #현재 구역의 ID
                start = np.array([vertical_lines[i], horizontal_lines[j]])
                end = np.array([vertical_lines[i + 1], horizontal_lines[j + 1]])

                reg = Reigon(start, end)

                #구역 내가 장애물이면 구역 추가에서 제외
                if self.grid[start[0]][start[1]] != 1:
                    for k in range(len(directionx)):
                        #경계 오류 방지
                        if i + directionx[k] < 0 or i + directionx[k] + 1 >= len(vertical_lines):
                            continue
                        if j + directiony[k] < 0 or j + 1 + directiony[k] >= len(horizontal_lines):
                            continue
                
                        #연결할 구역의 ID
                        start1 = np.array([vertical_lines[i + directionx[k]], horizontal_lines[j + directiony[k]]])
                        end1 = np.array([vertical_lines[i + 1 + directionx[k]], horizontal_lines[j + 1 + directiony[k]]])
                        #연결할 구역이 장애물이 아니여야 함
                        if self.grid[math.floor((start1[0] + end1[0]) / 2)][math.floor((start1[1] + end1[1]) / 2)] != 1 and self.getReigonID(start1, end1) in self.reigons :
                            if start[0] < end[0]:
                                reg1 = Reigon(start1, end1)
                            else:
                                reg1 = Reigon(end1, start1)

                            
                            self.reigons[reg.id].linkeds.append(reg1.id)
                            self.reigonsPopulation[reg.id] = 0

        

                 
                


                

