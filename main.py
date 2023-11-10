from Entity import Entity
from Draw import Drawer
from Map import Map
import random
import time
import numpy as np
import math
from aStar import aStar

#맵 생성

map = Map(np.array([80, 60]))

map.makeWall(np.array([25, 0]), np.array([28, 20]))
map.makeWall(np.array([20, 20]), np.array([35, 23]))
map.makeWall(np.array([20, 32]), np.array([35, 35]))
#map.makeWall(np.array([25, 32]), np.array([28, 48]))
map.makeWall(np.array([0, 45]), np.array([64, 48]))
map.makeWall(np.array([5, 32]), np.array([8, 48]))
map.makeWall(np.array([47, 32]), np.array([50, 48]))
map.makeWall(np.array([0, 50]), np.array([64, 53]))
map.makeWall(np.array([68, 0]), np.array([70, 55]))

map.makeregion()

#aStar 탐색을 위한 클래스 객체
astar = aStar(map)
 

#엔티티 생성

n = 100


e1 = [Entity(size=0.2) for i in range(n)]
for i in e1:
    i.setDestRange(np.array([44, 0]), np.array([64, 40]))
    i.setSpawnRange(np.array([0, 0]), np.array([20, 40]))

    i.position = i.randomDestination(i.spawnRangeStart, i.spawnRangeEnd, map, astar)
    map.reigonsPopulation[astar.getReigon(i.position)] += 1

    i.destination = i.randomDestination(i.destRangeStart, i.destRangeEnd, map, astar)
    i.normalColor = 'blue'

e2 = [Entity(size=0.2) for i in range(n)]
for i in e2:
    i.setDestRange(np.array([0, 0]), np.array([20, 40]))
    i.setSpawnRange(np.array([44, 0]), np.array([64, 40]))


    i.position = i.randomDestination(i.spawnRangeStart, i.spawnRangeEnd, map, astar)
    map.reigonsPopulation[astar.getReigon(i.position)] += 1

    i.destination = i.randomDestination(i.destRangeStart, i.destRangeEnd, map, astar)
    i.normalColor = 'purple'

Entities = e1 + e2


dr = Drawer(np.array([700, 600]))    

dt = 0.1


"""
while 1:
    #프레임 체크를 위한 시작 시간ç
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

        #Astar 경로 표시
        #for j in range(len(route) - 1):
        #    dr.DrawLine(np.array([route[j][0], route[j][1]])*10, np.array([route[j+1][0], route[j+1][1]])*10, 'green')

        #연결된 링크들 표시
        #for j in map.reigons[i].linkeds:
        #    dr.DrawLine(np.array([i[0], i[1]])*10, np.array([j[0], j[1]])*10, 'red')

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime

"""

isFire = False

def btnChange():
    print('btn click')
    dr.clickEvent(fire)

def fire(event):
    if True:
        mousepos = dr.mousePos()
        for i in e1 + e2:
            i.destination = np.array([mousepos[0], mousepos[1]])
            i.startedPos = i.position
            i.sq = astar.findRoute(i.startedPos, i.destination)
            i.tempDests = astar.routeToRandom(map, i.sq)
            i.nowTempDest = 0
            i.state = 'fire'
            i.destinations['fire'] = np.array([mousepos[0], mousepos[1]])


firebtn = dr.makeBtn("재난 발생", btnChange)
modebtn = dr.makeBtn("흐름 모드", btnChange)




while 1:
    #프레임 체크를 위한 시작 시간
    startTime = time.time()
    #화면 초기화
    dr.canvasClear()

    dr.coordinateText()
    ##메인 프로그램 작성

    for i in range(len(map.walls)):
        dr.DrawRectangle(map.walls[i].start * 10, map.walls[i].end * 10, 'black')
    
    #print(map.reigons.keys())

    #구역별 인구수 더하기
    map.addEntityReigon(astar, e1 + e2)

    #구역 표시하기
    for i in map.reigons.keys():
        d = map.regionDensity(i)
        dr.DrawRectangle(map.reigons[i].start * 10, map.reigons[i].end * 10, dr._from_rgb(255, 255 - d*400, 255 - d*400))
        #dr.DrawCircle(np.array([map.reigons[i].id[0], map.reigons[i].id[1]])* 10, 10, 'red')
        #for j in map.reigons[i].linkeds:
        #    dr.DrawLine(np.array([map.reigons[i].id[0], map.reigons[i].id[1]])*10, np.array([j[0], j[1]])*10, 'red')

    #엔티티 그리기
    for i in range(len(Entities)):
        ##맵 새로고침
        if map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] != 1:
            map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = 0

        Entities[i].move(dt, map, astar)

        ##맵 새로고침
        #print(Entities[i].position)
        map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = Entities[i]
        
        dr.DrawCircle(Entities[i].position * 10, Entities[i].size * 40, Entities[i].color)
        #dr.DrawCircle(Entities[i].destination * 10, Entities[i].size * 40, Entities[i].color)
        #dr.DrawCircle(Entities[i].tempDestination * 10, Entities[i].size * 40, Entities[i].color)

        #Astar 경로 표시
        #for j in range(len(e1[0].tempDests) - 1):
        #    dr.DrawLine(np.array([e1[0].tempDests[j][0], e1[0].tempDests[j][1]])*10, np.array([e1[0].tempDests[j+1][0], e1[0].tempDests[j+1][1]])*10, 'black')

        #for j in range(len(e1[0].sq) - 1):
        #    dr.DrawLine(np.array([e1[0].sq[j][0], e1[0].sq[j][1]])*10, np.array([e1[0].sq[j+1][0], e1[0].sq[j+1][1]])*10, 'black')


    #dr.window.title(str(1/dt))

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime

