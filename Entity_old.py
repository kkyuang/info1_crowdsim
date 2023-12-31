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
    def __init__(self, position, size, map):
        self.position = position.copy()
        self.size = size

        self.speed = 10
        self.destination = self.randomDestination(np.array([0, 0]), np.array([64, 48]), map)

        self.state = 'normal'

        self.randomnoise = np.array([random.random(), random.random()])

        self.color = 'black'
        self.normalColor = 'black'

        #현재 구역과 목적지의 구역. 0이면 초기상태.
        ##region id로.

        self.startedPos = position

        self.nowReigon = 0
        self.destReigon = 0

        #임시 목적지(길찾기에서)
        self.tempDestination = self.destination

        #들렸던 구역을 다시 들르지 않도록 제한
        self.visitedRegions = []

    def setDestRange(self, rangestart, rangeend):
        self.rangestart = rangestart
        self.rangeend = rangeend

    #범위 내부인지 판단
    def isinRange(self, position, rangestart, rangeend):
        if (rangestart[0] < position[0] and position[0] < rangeend[0]) and (rangestart[1] < position[1] and position[1] < rangeend[1]):
            return True
        else:
            return False

    #범위 내에서 랜덤인 목적지를 설정
    def randomDestination(self, rangestart, rangeend, map):
        while True:
            dest = np.array([random.uniform(rangestart[0], rangeend[0]), random.uniform(rangestart[1], rangeend[1])])
            if map.grid[math.floor(dest[0])][math.floor(dest[1])] == 0:
                return dest

    def move(self, dt, map: Map):
        velocity = np.array([0, 0])

        ##일반적 배회 상태 알고리즘
        if self.state == 'normal':

            #현재 위치한 구역
            def getReigon(position):
                myReigonStart = np.array([0, 0])
                myReigonEnd = np.array([0, 0])
                for i in range(len(map.vertical_lines)-1):
                    if map.vertical_lines[i] <= position[0] and position[0] < map.vertical_lines[i + 1]:
                        myReigonStart[0] = map.vertical_lines[i]
                        myReigonEnd[0] = map.vertical_lines[i+1]

                for i in range(len(map.horizontal_lines)-1):
                    if map.horizontal_lines[i] <= position[1] and position[1] < map.horizontal_lines[i + 1]:
                        myReigonStart[1] = map.horizontal_lines[i]
                        myReigonEnd[1] = map.horizontal_lines[i+1]

                return map.getReigonID(myReigonStart, myReigonEnd)
            
            #목적지 정하기 -> 최종 목적지를 향한 다음 구역 탐색 A* 알고리즘
            #처음 실행시 -> 현재 구역의 id 얻기 및 목적지의 id 얻기
            #print(self.nowReigon == getReigon(self.position))
            #self.nowReigon == getReigon(self.position) or 
            if self.nowReigon == getReigon(self.position) or self.nowReigon == 0:
                self.nowReigon = getReigon(self.position)
                self.destReigon = getReigon(self.destination)
                print('reach')
            
                #목적지와 같은 구역에 속해 있지 않을 때 임시 목표를 정함
                if self.nowReigon == self.destReigon:
                    self.tempDestination = self.destination
                else:
                    #구역 범위에서 A* 알고리즘 적용
                    #현재 구역에서 연결된 구역으로
                    costs = [0 for i in range(len(map.reigons[self.nowReigon].linkeds))]
                    k = 0
                    for i in map.reigons[self.nowReigon].linkeds:
                        #현재와의 거리
                        g = norm(self.startedPos, np.array([i[0], i[1]]))
                        #목적지까지의 거리
                        h = norm(self.destination, np.array([i[0], i[1]]))

                        costs[k] = g + k + (self.visitedRegions[i] if i in self.visitedRegions.keys() else 0)
                        k+=1
                    
                    #최솟값 구하기
                    minV = 0
                    for i in range(len(costs)):
                        if costs[i] < costs[minV]:
                            minV = i
                        
                    #구역 및 임시 목적지 변경하기
                    if len(costs) > 0:
                        self.nowReigon = map.reigons[self.nowReigon].linkeds[minV]
                        for i in self.visitedRegions.keys():
                            self.visitedRegions[i] *= 0.5
                        if self.nowReigon in self.visitedRegions.keys():
                            self.visitedRegions[self.nowReigon] += 1000
                        else:
                            self.visitedRegions[self.nowReigon] = 1000
                        #구역 내에서 랜덤하게
                        self.tempDestination = self.randomDestination(map.reigons[self.nowReigon].start, map.reigons[self.nowReigon].end, map)
                        #self.tempDestination = np.array([self.nowReigon[0], self.nowReigon[1]])
                    


                




            #A* 알고리즘 사용하기
            #탐색 지점이 빈 공간일 때만 cost함수를 계산, 장애물이 존재할 때는 -1으로 한다.
            #탐색범위 순서: 좌상0, 상1, 우상2, 좌3, 우4, 좌하5, 하6, 우하7
            cost = [0 for i in range(8)]
        

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
                        h = norm(search, self.tempDestination)
                        cost[k] = g + h
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
                    

            #목적지 접근 시 목적지 변경
            if np.linalg.norm(self.destination - self.position) < self.speed:
                print('dest!')
                self.destination = self.randomDestination(self.rangestart, self.rangeend, map)
                self.destReigon = 0
                self.nowReigon = 0
                self.visitedRegions = {}


            #벡터 졍규화
            if np.linalg.norm(direction) != 0:
                direction = (direction) / np.linalg.norm(direction)

            velocity = direction * self.speed

        #목적지 방향으로 미소거리 더하기
        newposition = self.position + velocity * dt
        #if map.grid[math.floor(newposition[0])][math.floor(newposition[1])] == 0:
        self.position = newposition
        self.startedPos = newposition