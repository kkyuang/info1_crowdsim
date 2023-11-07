from Entity import Entity
from Draw import Drawer
from Map import Map
import random
import time
import numpy as np
import math
from aStar import aStar

#맵 생성

map = Map(np.array([700, 500]))

map.makeWall(np.array([25, 0]), np.array([28, 20]))
map.makeWall(np.array([20, 20]), np.array([35, 23]))
map.makeWall(np.array([20, 32]), np.array([35, 35]))
map.makeWall(np.array([25, 32]), np.array([28, 48]))
map.makeWall(np.array([0, 45]), np.array([64, 48]))

map.makeregion()
 

#엔티티 생성

n = 1


e1 = [Entity(position=np.array([random.uniform(0, 20), random.uniform(0, 40)]), size=0.2, map=map) for i in range(n)]
for i in e1:
    i.setDestRange(np.array([44, 0]), np.array([64, 40]))
    i.destination = i.randomDestination(i.rangestart, i.rangeend, map)
    i.normalColor = 'blue'

e2 = [Entity(position=np.array([random.uniform(44, 64), random.uniform(0, 40)]), size=0.2, map=map) for i in range(n)]
for i in e2:
    i.setDestRange(np.array([0, 0]), np.array([20, 40]))
    i.destination = i.randomDestination(i.rangestart, i.rangeend, map)
    i.normalColor = 'purple'

Entities = e1 + e2


dr = Drawer(np.array([640, 480]))    

dt = 0.1

startPosition = 0

#aStar 탐색을 위한 클래스 객체
astar = aStar(map)

route = astar.findRoute(e1[0].startedPos, e1[0].destination)
print(route)


while 1:
    #프레임 체크를 위한 시작 시간
    startTime = time.time()
    #화면 초기화
    dr.canvasClear()

    ##메인 프로그램 작성

    for i in range(len(map.walls)):
        dr.DrawRectangle(map.walls[i].start * 10, map.walls[i].end * 10, 'black')
    
    #print(map.reigons.keys())
    for i in map.reigons.keys():
        dr.DrawRectangle2(map.reigons[i].start * 10, map.reigons[i].end * 10, 'red')
        dr.DrawCircle(np.array([map.reigons[i].id[0], map.reigons[i].id[1]])* 10, 10, 'red')

        for j in range(len(route) - 1):
            dr.DrawLine(np.array([route[j][0], route[j][1]])*10, np.array([route[j+1][0], route[j+1][1]])*10, 'green')

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime



"""
while 1:
    #프레임 체크를 위한 시작 시간
    startTime = time.time()
    #화면 초기화
    dr.canvasClear()

    ##메인 프로그램 작성

    for i in range(len(map.walls)):
        dr.DrawRectangle(map.walls[i].start * 10, map.walls[i].end * 10, 'black')
    
    #print(map.reigons.keys())
    for i in map.reigons.keys():
        dr.DrawRectangle2(map.reigons[i].start * 10, map.reigons[i].end * 10, 'red')
        dr.DrawCircle(np.array([map.reigons[i].id[0], map.reigons[i].id[1]])* 10, 10, 'red')
        for j in map.reigons[i].linkeds:
            dr.DrawLine(np.array([map.reigons[i].id[0], map.reigons[i].id[1]])*10, np.array([j[0], j[1]])*10, 'red')

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
        #dr.DrawCircle(Entities[i].destination * 10, Entities[i].size * 40, Entities[i].color)
        #dr.DrawCircle(Entities[i].tempDestination * 10, Entities[i].size * 40, Entities[i].color)

    #dr.window.title(str(1/dt))

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime

"""