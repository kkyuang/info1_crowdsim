import numpy as np
import random
import math 

class Entity:
    def __init__(self, position, size):
        self.position = position.copy()
        self.size = size

        self.speed = 4
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
            #목적지를 향하는 방향 구하기
            direction = self.destination - self.position + self.randomnoise

            #목적지 접근 시 목적지 변경
            if np.linalg.norm(direction) < self.speed:
                self.destination = self.randomDestination(self.rangestart, self.rangeend)

            #벡터 졍규화
            direction = (direction) / np.linalg.norm(direction)

            velocity = direction * self.speed

        ##충돌 처리 관련

        #회피 방향
        avoidDirection = np.array([0, 0])
        #충돌 여부
        isCollision = False
        #경계 여부
        isBorder = False

        #경계 충돌 판정
        if math.floor(self.position[0]) <= 0:
            avoidDirection = avoidDirection + np.array([1, 0])
            isBorder = True
        if math.floor(self.position[0]) >= map.size[0] - 1:
            avoidDirection = avoidDirection + np.array([-1, 0])
            isBorder = True
        if math.floor(self.position[1]) <= 0:
            avoidDirection = avoidDirection + np.array([0, 1])
            isBorder = True
        if math.floor(self.position[1]) >= map.size[1] - 1:
            avoidDirection = avoidDirection + np.array([0, -1])
            isBorder = True
        
        if not isBorder:
            #개체 및 장애물 충돌 판정
            if map.grid[math.floor(self.position[0]) - 1][math.floor(self.position[1]) - 1] != 0:
                avoidDirection = avoidDirection + np.array([1, 1]) * 1.414
                isCollision = True
            if map.grid[math.floor(self.position[0])][math.floor(self.position[1]) - 1] != 0:
                avoidDirection = avoidDirection + np.array([0, 1])
                isCollision = True
            if map.grid[math.floor(self.position[0]) - 1][math.floor(self.position[1])] != 0:
                avoidDirection = avoidDirection + np.array([1, 0])
                isCollision = True
            if map.grid[math.floor(self.position[0]) + 1][math.floor(self.position[1]) + 1] != 0:
                avoidDirection = avoidDirection + np.array([-1, -1]) * 1.414
                isCollision = True
            if map.grid[math.floor(self.position[0])][math.floor(self.position[1]) + 1] != 0:
                avoidDirection = avoidDirection + np.array([0, -1])
                isCollision = True
            if map.grid[math.floor(self.position[0]) + 1][math.floor(self.position[1])] != 0:
                avoidDirection = avoidDirection + np.array([-1, 0])
                isCollision = True
            if map.grid[math.floor(self.position[0]) + 1][math.floor(self.position[1]) - 1] != 0:
                avoidDirection = avoidDirection + np.array([-1, 1]) * 1.414
                isCollision = True
            if map.grid[math.floor(self.position[0]) - 1][math.floor(self.position[1]) + 1] != 0:
                avoidDirection = avoidDirection + np.array([1, -1]) * 1.414
                isCollision = True

        
        if isCollision:
            if (np.linalg.norm(avoidDirection)) != 0:
                velocity = (avoidDirection / (np.linalg.norm(avoidDirection))) * self.speed
            self.color = 'red'

        else:
            self.color = self.normalColor
            
            

        #목적지 방향으로 미소거리 더하기
        self.position = self.position + velocity * dt
        


    
    