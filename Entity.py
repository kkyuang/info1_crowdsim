import numpy as np
from Map import Map
from Map import Reigon
import random
import math
from aStar import aStar 

def norm(a, b):
    #유클리드 거리
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    #택시 거리
    #return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Entity:
    def __init__(self, size):
        self.size = size

        self.speed = 3
        #self.destination = self.randomDestination(np.array([0, 0]), np.array([64, 48]), map)
        self.destination = 0
        self.state = 'normal'

        self.randomnoise = np.array([random.random(), random.random()])

        self.color = 'black'
        self.normalColor = 'black'

        #현재 구역과 목적지의 구역. 0이면 초기상태.
        ##region id로.

        self.nowReigon = 0
        self.destReigon = 0

        #임시 목적지 목록(길찾기에서)
        self.tempDests = 0
        self.nowTempDest = 0

        #들렸던 구역을 다시 들르지 않도록 제한
        self.visitedRegions = []


    def setSpawnRange(self, rangestart, rangeend):
        self.spawnRangeStart = rangestart
        self.spawnRangeEnd = rangeend

    def setDestRange(self, rangestart, rangeend):
        self.destRangeStart = rangestart
        self.destRangeEnd = rangeend

    #범위 내부인지 판단
    def isinRange(self, position, rangestart, rangeend):
        if (rangestart[0] < position[0] and position[0] < rangeend[0]) and (rangestart[1] < position[1] and position[1] < rangeend[1]):
            return True
        else:
            return False

    #범위 내에서 랜덤인 목적지를 설정
    def randomDestination(self, rangestart, rangeend, map, astar: aStar):
        while True:
            dest = np.array([random.uniform(rangestart[0], rangeend[0]), random.uniform(rangestart[1], rangeend[1])])
            if astar.isinReigon(dest, map):
                return dest

    def move(self, dt, map: Map, astar: aStar):
        velocity = np.array([0, 0])

        ##일반적 배회 상태 알고리즘
        if self.state == 'normal':

            if np.linalg.norm(self.destination - self.position) < self.speed or self.tempDests == 0:

                self.destination = self.randomDestination(self.destRangeStart, self.destRangeEnd, map, astar)
                self.position = self.randomDestination(self.spawnRangeStart, self.spawnRangeEnd, map, astar)
                self.startedPos = self.position

                sq = astar.findRoute(self.startedPos, self.destination)
                self.tempDests = astar.routeToRandom(map, sq)
                self.nowTempDest = 0


            #목적지 접근 시 목적지 변경
            if np.linalg.norm(self.tempDests[self.nowTempDest] - self.position) < 2:
                if self.nowTempDest < len(self.tempDests) - 1:
                    self.nowTempDest += 1
                #마지막 구역에서는?
                if self.nowTempDest == len(self.tempDests) - 1:
                    #최종 목적지를 임시 목적지로 함.
                    self.tempDests[self.nowTempDest] = self.destination


            #탐색 지점이 빈 공간일 때만 cost함수를 계산, 장애물이 존재할 때는 -1으로 한다.
            #탐색범위 순서: 좌상0, 상1, 우상2, 좌3, 우4, 좌하5, 하6, 우하7
            """cost = [0 for i in range(8)]
        

            #경계 충돌 판정
            if math.floor(self.position[0]) <= 1: #좌측에 경계 존재
                cost[0] = -1 #좌상
                cost[3] = -1 #좌
                cost[5] = -1 #좌하
            if math.floor(self.position[0]) >= map.size[0] - 2: #우측에 경계 존재
                cost[2] = -1 #우상
                cost[4] = -1 #우
                cost[7] = -1 #우하
            if math.floor(self.position[1]) <= 1: #하단에 경계 존재
                cost[5] = -1 #좌하
                cost[6] = -1 #하
                cost[7] = -1 #우하
            if math.floor(self.position[1]) >= map.size[1] - 2: #상단에 경계 존재
                cost[0] = -1 #좌상
                cost[1] = -1 #상
                cost[2] = -1 #우상


            directionx = [-1, 0, 1, -1, 1, -1, 0, 1]
            directiony = [1, 1, 1, 0, 0, -1, -1, -1]

            for k in range(8):
                if cost[k] != -1:
                    if map.grid[math.floor(self.position[0]) + directionx[k]][math.floor(self.position[1]) + directiony[k]] == 0:
                        #비용 계산
                        if directionx[k]*directiony[k] == 0:
                            g = 1
                        else:
                            g = 1.4

                        search = np.array([math.floor(self.position[0]) + directionx[k] + 0.5, math.floor(self.position[1])  + directiony[k] + 0.5])
                        h = norm(search, self.tempDests[self.nowTempDest])
                        cost[k] = h
                    else:
                        cost[k] = -1

            direction = np.array([0, 0])

            #최소의 cost값 탐색
            minC = 0
            for i in range(8):
                if cost[i] != -1:
                    minC = i

            if minC != 0: #탐색 가능한 공간이 있는 경우
                for i in range(8):
                    if cost[i] != -1 and cost[i] < cost[minC]:
                        minC = i
                
                directions = {0: np.array([-1, 1]),  1: np.array([0, 1]),  2: np.array([1, 1]),
                              3: np.array([-1, 0]),                        4: np.array([0, 1]),
                              5: np.array([-1, -1]), 6: np.array([0, -1]), 7: np.array([1, -1])}

                #최솟값의 방향에 따라서 개체의 이동 방향을 정함
                direction = directions[minC]
                self.color = self.normalColor
            
            else: #사방이 장애물로 둘러싸인 경우
                self.color = "red"
                pass
                    """
        
            self.color = self.normalColor
            direction = (self.tempDests[self.nowTempDest] - self.position) / norm(self.position, self.tempDests[self.nowTempDest])


            #벡터 졍규화
            if np.linalg.norm(direction) != 0:
                direction = (direction) / np.linalg.norm(direction)

            velocity = direction * self.speed

        #목적지 방향으로 미소거리 더하기
        newposition = self.position + velocity * dt
        #if map.grid[math.floor(newposition[0])][math.floor(newposition[1])] == 0:
        self.position = newposition
        self.startedPos = newposition