from Entity import Entity
from Draw import Drawer
from Map import Map
import random
import time
import numpy as np
import math

#맵 생성

map = Map(np.array([700, 500]))

map.makeWall(np.array([25, 0]), np.array([28, 20]))
map.makeWall(np.array([20, 20]), np.array([35, 23]))
map.makeWall(np.array([20, 32]), np.array([35, 35]))
map.makeWall(np.array([25, 32]), np.array([28, 48]))
map.makeWall(np.array([0, 45]), np.array([64, 46]))

map.makeregion()


#엔티티 생성

n = 20


e1 = [Entity(position=np.array([random.randrange(0, 20), random.randrange(0, 48)]), size=0.2, map=map) for i in range(n)]
for i in e1:
    i.setDestRange(np.array([44, 0]), np.array([64, 48]))
    i.destination = i.randomDestination(i.rangestart, i.rangeend, map)
    i.normalColor = 'blue'

e2 = [Entity(position=np.array([random.randrange(44, 64), random.randrange(0, 48)]), size=0.2, map=map) for i in range(n)]
for i in e2:
    i.setDestRange(np.array([0, 0]), np.array([20, 48]))
    i.destination = i.randomDestination(i.rangestart, i.rangeend, map)
    i.normalColor = 'purple'

Entities = e1 + e2


dr = Drawer(np.array([640, 480]))    

dt = 0.1

startPosition = 0
while 1:
    #프레임 체크를 위한 시작 시간
    startTime = time.time()
    #화면 초기화
    dr.canvasClear()

    ##메인 프로그램 작성

    for i in range(len(map.walls)):
        dr.DrawRectangle(map.walls[i].start * 10, map.walls[i].end * 10, 'black')
    
    for i in map.reigons.keys():
        dr.DrawRectangle(map.reigons[i].start * 10, map.reigons[i].end * 10, 'gray')

    #엔티티 그리기
    for i in range(len(Entities)):
        ##맵 새로고침
        if map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] != 1:
            map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = 0

        Entities[i].move(dt, map)

        ##맵 새로고침
        #print(Entities[i].position)
        map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = Entities[i]
        
        dr.DrawCircle(Entities[i].position * 10, Entities[i].size * 40, Entities[i].color)

    #dr.window.title(str(1/dt))

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime