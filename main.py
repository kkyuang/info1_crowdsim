from Entity import Entity
from Draw import Drawer
from Map import Map
import random
import time
import numpy as np
import math


n = 20

e1 = [Entity(position=np.array([random.randrange(0, 20), random.randrange(0, 48)]), size=0.2) for i in range(n)]
for i in e1:
    i.setDestRange(np.array([44, 0]), np.array([64, 48]))
    i.destination = i.randomDestination(i.rangestart, i.rangeend)
    i.normalColor = 'blue'

e2 = [Entity(position=np.array([random.randrange(44, 64), random.randrange(0, 48)]), size=0.2) for i in range(n)]
for i in e2:
    i.setDestRange(np.array([0, 0]), np.array([20, 48]))
    i.destination = i.randomDestination(i.rangestart, i.rangeend)

Entities = e1 + e2
map = Map(np.array([64, 48]))

dr = Drawer(np.array([640, 480]))        

dt = 0.1

startPosition = 0
while 1:
    #프레임 체크를 위한 시작 시간
    startTime = time.time()
    #화면 초기화
    dr.canvasClear()

    ##메인 프로그램 작성

    #엔티티 그리기
    for i in range(len(Entities)):
        ##맵 새로고침
        map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = 0

        Entities[i].move(dt, map)

        ##맵 새로고침
        map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = Entities[i]
        
        dr.DrawCircle(Entities[i].position * 10, Entities[i].size * 100, Entities[i].color)

    dr.DrawRectangle(np.array([19, 29]), np.array([299, 49]), 'black')

    #dr.window.title(str(1/dt))

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime