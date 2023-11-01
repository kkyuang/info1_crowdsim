import numpy as np
import random

class Entity:
    def __init__(self, position, size, destination):
        self.position = position.copy()
        self.size = size

        self.speed = 1
        self.destination = destination

        self.randomnoise = np.array([random.random(), random.random()])

    def move(self):
        #목적지를 향하는 방향 구하기
        direction = self.destination - self.position + self.randomnoise
        direction = (direction) / np.linalg.norm(direction)

        #목적지 방향으로 미소거리 더하기
        self.position = self.position + direction * self.speed * 0.01

    
    