import numpy as np
import random
import math

def norm(a, b):
    #유클리드 거리
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    #택시 거리
    #return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Entity:
    def __init__(self, position, size):
        self.position = position.copy()
        self.size = size

        self.speed = 10
        self.destination = self.randomDestination(np.array([0, 0]), np.array([64, 48]))

        self.state = 'normal'

        self.randomnoise = np.array([random.random(), random.random()])

        self.color = 'black'
        self.normalColor = 'black'

    def setDestRange(self, rangestart, rangeend):
        self.rangestart = rangestart
        self.rangeend = rangeend

    #범위 내에서 랜덤인 목적지를 설정
    def randomDestination(self, rangestart, rangeend):
        return np.array([random.randrange(rangestart[0], rangeend[0]), random.randrange(rangestart[1], rangeend[1])])

    def move(self, dt, map):
        velocity = np.array([0, 0])

        ##일반적 배회 상태 알고리즘
        if self.state == 'normal':
            #A* 알고리즘 사용하기
            #탐색 지점이 빈 공간일 때만 cost함수를 계산, 장애물이 존재할 때는 -1으로 한다.
            #탐색범위 순서: 좌상0, 상1, 우상2, 좌3, 우4, 좌하5, 하6, 우하7
            cost = [0 for i in range(8)]
        

            #경계 충돌 판정
            if math.floor(self.position[0]) <= 0: #좌측에 경계 존재
                cost[0] = -1 #좌상
                cost[3] = -1 #좌
                cost[5] = -1 #좌하
            if math.floor(self.position[0]) >= map.size[0] - 1: #우측에 경계 존재
                cost[2] = -1 #우상
                cost[4] = -1 #우
                cost[7] = -1 #우하
            if math.floor(self.position[1]) <= 0: #하단에 경계 존재
                cost[5] = -1 #좌하
                cost[6] = -1 #하
                cost[7] = -1 #우하
            if math.floor(self.position[1]) >= map.size[1] - 1: #상단에 경계 존재
                cost[0] = -1 #좌상
                cost[1] = -1 #상
                cost[2] = -1 #우상


            #좌상 탐색
            if cost[0] != -1:
                if map.grid[math.floor(self.position[0]) - 1][math.floor(self.position[1]) + 1] == 0:
                    #비용 계산
                    g = 1.4
                    search = np.array([math.floor(self.position[0]) - 1 + 0.5, math.floor(self.position[1]) + 1 + 0.5])
                    h = norm(search, self.destination)
                    cost[0] = g + h
                else:
                    cost[0] = -1

            #상 탐색
            if cost[1] != -1:
                if map.grid[math.floor(self.position[0])][math.floor(self.position[1]) + 1] == 0:
                    #비용 계산
                    g = 1
                    search = np.array([math.floor(self.position[0]) + 0.5, math.floor(self.position[1]) + 1 + 0.5])
                    h = norm(search, self.destination)
                    cost[1] = g + h
                else:
                    cost[1] = -1

            #우상 탐색
            if cost[2] != -1:
                if map.grid[math.floor(self.position[0]) + 1][math.floor(self.position[1]) + 1] == 0:
                    #비용 계산
                    g = 1
                    h = norm(np.array([math.floor(self.position[0]) + 1 + 0.5, math.floor(self.position[1]) + 1 + 0.5]), self.destination)
                    cost[2] = g + h
                else:
                    cost[2] = -1

            #좌 탐색
            if cost[3] != -1:
                if map.grid[math.floor(self.position[0]) - 1][math.floor(self.position[1])] == 0:
                    #비용 계산
                    g = 1
                    h = norm(np.array([math.floor(self.position[0]) - 1 + 0.5, math.floor(self.position[1]) + 0.5]), self.destination)
                    cost[3] = g + h
                else:
                    cost[3] = -1

            #우 탐색
            if cost[4] != -1:
                if map.grid[math.floor(self.position[0]) + 1][math.floor(self.position[1])] == 0:
                    #비용 계산
                    g = 1
                    h = norm(np.array([math.floor(self.position[0]) + 1 + 0.5, math.floor(self.position[1]) + 0.5]), self.destination)
                    cost[4] = g + h
                else:
                    cost[4] = -1

            #좌하 탐색
            if cost[5] != -1:
                if map.grid[math.floor(self.position[0]) - 1][math.floor(self.position[1]) - 1] == 0:
                    #비용 계산
                    g = 1
                    h = norm(np.array([math.floor(self.position[0]) - 1 + 0.5, math.floor(self.position[1]) - 1 + 0.5]), self.destination)
                    cost[5] = g + h
                else:
                    cost[5] = -1

            #하 탐색
            if cost[6] != -1:
                if map.grid[math.floor(self.position[0])][math.floor(self.position[1]) - 1] == 0:
                    #비용 계산
                    g = 1
                    h = norm(np.array([math.floor(self.position[0]) + 0.5, math.floor(self.position[1]) - 1 + 0.5]), self.destination)
                    cost[6] = g + h
                else:
                    cost[6] = -1

            #우하 탐색
            if cost[7] != -1:
                if map.grid[math.floor(self.position[0]) + 1][math.floor(self.position[1]) - 1] == 0:
                    #비용 계산
                    g = 1
                    h = norm(np.array([math.floor(self.position[0]) + 1 + 0.5, math.floor(self.position[1]) - 1 + 0.5]), self.destination)
                    cost[7] = g + h
                else:
                    cost[7] = -1


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
                self.destination = self.randomDestination(self.rangestart, self.rangeend)

            #벡터 졍규화
            if np.linalg.norm(direction) != 0:
                direction = (direction) / np.linalg.norm(direction)

            velocity = direction * self.speed

        #목적지 방향으로 미소거리 더하기
        newposition = self.position + velocity * dt
        if map.grid[math.floor(newposition[0])][math.floor(newposition[1])] == 0:
            self.position = newposition
        


    
    