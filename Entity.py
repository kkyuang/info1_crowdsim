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

        self.speed = 100
        #self.destination = self.randomDestination(np.array([0, 0]), np.array([64, 48]), map)
        self.destination = 0
        self.state = 'normal'
        self.mode = 'current'

        #'stop mode'에서 현재 움직이고 있는가 하는 상태를 나타냄
        self.isMoving = True

        #'disappear mode'에서 이제 삭제되어야 하는가 하는 것을 나타냄
        self.willbeDisappear = False

        self.randomnoise = np.array([random.random(), random.random()])

        self.color = 'black'
        self.normalColor = 'black'

        self.sq = []

        #현재 구역과 목적지의 구역. 0이면 초기상태.
        ##region id로.

        self.nowReigon = 0
        self.destReigon = 0

        #임시 목적지 목록(길찾기에서)
        self.tempDests = 0
        self.nowTempDest = 0

        #들렸던 구역을 다시 들르지 않도록 제한
        self.visitedRegions = []
        self.destinations = {}


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
            
    #삭제시
    def __del__(self):
        #print('deleted')
        pass

    def move(self, dt, map: Map, astar: aStar):
        velocity = np.array([0, 0])

        ##일반적 배회 상태 알고리즘
        if True:
            #최초 생성시
            if self.tempDests == 0:
                #위치 범위 내에서 랜덤으로 설정
                self.position = self.randomDestination(self.spawnRangeStart, self.spawnRangeEnd, map, astar)
                self.startedPos = self.position

                #경로 찾기
                self.sq = astar.findRoute(self.startedPos, self.destination)
                self.tempDests = astar.routeToRandom(map, self.sq)
                self.nowTempDest = 0

            elif np.linalg.norm(self.destination - self.position) < self.speed:
                #배회모드: 랜덤으로 목적지만 설정
                if self.mode == 'roaming':
                    self.destination = self.randomDestination(self.destRangeStart, self.destRangeEnd, map, astar)
                #흐름모드: 랜덤으로 목적지, 시작지점 다시 설정
                elif self.mode == 'current':
                    self.position = self.randomDestination(self.spawnRangeStart, self.spawnRangeEnd, map, astar)
                    if self.state == 'fire':
                        self.destination = self.destinations[self.state]
                    else:
                        self.destination = self.randomDestination(self.destRangeStart, self.destRangeEnd, map, astar)
                #삭제모드: 도착시 아예 사라짐
                elif self.mode == 'disappear':
                    self.willbeDisappear = True
                #중지모드: 도착시 움직임을 종료함
                if self.mode == 'stop':
                    self.isMoving = False
                else:
                    self.isMoving = True


                self.startedPos = self.position

                #경로 찾기
                if (not self.isMoving) or self.willbeDisappear:
                    return
                
                self.sq = astar.findRoute(self.startedPos, self.destination)
                self.tempDests = astar.routeToRandom(map, self.sq)
                self.nowTempDest = 0

            if (not self.isMoving) or self.willbeDisappear:
                return


            #목적지 접근 시 목적지 변경
            if np.linalg.norm(self.tempDests[self.nowTempDest] - self.position) < 2:
                if self.nowTempDest < len(self.tempDests) - 1:
                    self.nowTempDest += 1
                #마지막 구역에서는?
                if self.nowTempDest == len(self.tempDests) - 1:
                    #최종 목적지를 임시 목적지로 함.
                    self.tempDests[self.nowTempDest] = self.destination

        
            self.color = self.normalColor
            direction = (self.tempDests[self.nowTempDest] - self.position) / norm(self.position, self.tempDests[self.nowTempDest])


            #벡터 졍규화
            if np.linalg.norm(direction) != 0:
                direction = (direction) / np.linalg.norm(direction)

            velocity = direction * self.speed
            
        self.nowReigon = astar.getReigon(self.position)
        if self.nowReigon in map.reigons.keys():
            self.speed = 3/(1 + (map.regionDensity(self.nowReigon)))
        else:
            self.speed = 3/(1)
        #목적지 방향으로 미소거리 더하기
        newposition = self.position + velocity * dt
        #if map.grid[math.floor(newposition[0])][math.floor(newposition[1])] == 0:
        self.position = newposition
        self.startedPos = newposition

        