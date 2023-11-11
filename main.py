from Entity import Entity
from Draw import Drawer
from Map import Map
import random
import time
import numpy as np
import math
from aStar import aStar
import pickle

#맵 생성

MapElements = {}
with open('MapTemp',"rb") as fr:
    MapElements = pickle.load(fr)
    
map = Map(np.array([MapElements['size'][0], MapElements['size'][1]]))

for i in MapElements[1]:
    map.makeWall(np.array([i[0][0], i[0][1]]), np.array([i[1][0], i[1][1]]))
for i in MapElements[2]:
    map.makeShelter(np.array([i[0][0], i[0][1]]), np.array([i[1][0], i[1][1]]))

map.makeregion()

#aStar 탐색을 위한 클래스 객체
astar = aStar(map)
 

#전체 엔티티 목록
Entities = []

#군중 그룹 생성
n = int(input("군중 그룹의 수를 입력해주세요. : "))
for k in range(1, n + 1):
    print("\n\n군중 그룹 " + str(k) + "번을 생성하겠습니다.")
    popul = int(input("군중 그룹 " + str(k) + "의 인구수를 입력해주세요. : "))
    startR = int(input("군중 그룹 " + str(k) + "의 시작 구역을 입력해주세요. (3, 4, 5, 6) : "))
    destR = int(input("군중 그룹 " + str(k) + "의 목적 구역을 입력해주세요. (3, 4, 5, 6) : "))
    color = input("군중 그룹 " + str(k) + "의 색을 입력해주세요. : ")

    e1 = [Entity(size=0.2) for i in range(popul)]
    for i in e1:
        i.setDestRange(np.array([MapElements[startR][0][0][0], MapElements[startR][0][0][1]]), np.array([MapElements[startR][0][1][0], MapElements[startR][0][1][1]]))
        i.setSpawnRange(np.array([MapElements[destR][0][0][0], MapElements[destR][0][0][1]]), np.array([MapElements[destR][0][1][0], MapElements[destR][0][1][1]]))

        i.position = i.randomDestination(i.spawnRangeStart, i.spawnRangeEnd, map, astar)
        map.reigonsPopulation[astar.getReigon(i.position)] += 1

        i.destination = i.randomDestination(i.destRangeStart, i.destRangeEnd, map, astar)
        i.normalColor = color

    Entities += e1


screenSize = np.array([700, 600])
dr = Drawer(screenSize)    

#화면 확대 배율
DPscale = screenSize[0] / map.size[0]

dt = 0.1


def btnChange():
    print('btn click')
    dr.clickEvent(fire)

def fire(event):
    if True:
        mousepos = dr.mousePos()
        for i in Entities:
            i.destination = np.array([mousepos[0] / DPscale, mousepos[1] / DPscale])
            print(i.destination)
            i.startedPos = i.position
            i.sq = astar.findRoute(i.startedPos, i.destination)
            i.tempDests = astar.routeToRandom(map, i.sq)
            i.nowTempDest = 0
            i.state = 'fire'
            i.destinations['fire'] = np.array([mousepos[0] / DPscale, mousepos[1] / DPscale])




Mode = "current" #기본적으로 흐름 모드
#모드 변경 순서
ModeTable = {"current": "disappear", "disappear": "stop", "stop": "roaming", "roaming":"current"}
#모드 한국어
ModeBtnName = {"current": "흐름 모드", "disappear": "소멸 모드", "stop": "정지 모드", "roaming":"배회 모드"}


#모드를 순회적으로 변경하는 함수
def setMode():
    global Mode
    Mode = ModeTable[Mode]
    modebtn.config(text=ModeBtnName[Mode])

    #모드 설정
    for i in Entities:
        i.mode = Mode
    

#재난 발생 토글
isFire = False

firebtn = dr.makeBtn("목적지 설정", btnChange)
firebtn = dr.makeBtn("개인별 대피", btnChange)
firebtn = dr.makeBtn("중앙 통제 대피", btnChange)
modebtn = dr.makeBtn("흐름 모드", setMode)





while 1:
    #프레임 체크를 위한 시작 시간
    startTime = time.time()
    #화면 초기화
    dr.canvasClear()

    dr.coordinateText(DPscale)
    ##메인 프로그램 작성

    #벽 그리기
    for i in range(len(map.walls)):
        dr.DrawRectangle(map.walls[i].start * DPscale, map.walls[i].end * DPscale, 'black')
    
    #print(map.reigons.keys())

    #구역별 인구수 더하기
    map.addEntityReigon(astar, Entities)

    #구역 표시하기
    for i in map.reigons.keys():
            
        d = map.regionDensity(i)
        #print(d)
        dr.DrawRectangle(map.reigons[i].start * DPscale, map.reigons[i].end * DPscale, dr._from_rgb(255, 255 - d*20, 255 - d*20))
        
            
        #디버그용
        #dr.DrawCircle(np.array([map.reigons[i].id[0], map.reigons[i].id[1]])* DPscale, DPscale / 10, 'red')
        #for j in map.reigons[i].linkeds:
        #    dr.DrawLine(np.array([map.reigons[i].id[0], map.reigons[i].id[1]])*DPscale, np.array([j[0], j[1]])*DPscale, 'red')

    #대피소 그리기
    for i in range(len(map.shelters)):
        dr.DrawRectangle(map.shelters[i].start * DPscale, map.shelters[i].end * DPscale, '#00ff00')


    #엔티티 그리기
    for i in range(len(Entities)):
        ##맵 새로고침
        #if map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] != 1:
        #    map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = 0

        Entities[i].move(dt, map, astar)

        ##맵 새로고침
        #print(Entities[i].position)
        #map.grid[math.floor(Entities[i].position[0])][math.floor(Entities[i].position[1])] = Entities[i]
        
        dr.DrawCircle(Entities[i].position * DPscale, Entities[i].size * DPscale, Entities[i].color)
        #dr.DrawCircle(Entities[i].destination * DPscale, Entities[i].size * DPscale, Entities[i].color)
        #dr.DrawCircle(Entities[i].tempDestination * DPscale, Entities[i].size * DPscale, Entities[i].color)

        #Astar 경로 표시
        #for j in range(len(e1[0].tempDests) - 1):
        #    dr.DrawLine(np.array([e1[0].tempDests[j][0], e1[0].tempDests[j][1]])*DPscale, np.array([e1[0].tempDests[j+1][0], e1[0].tempDests[j+1][1]])*DPscale, 'black')

        #for j in range(len(e1[0].sq) - 1):
        #    dr.DrawLine(np.array([e1[0].sq[j][0], e1[0].sq[j][1]])*DPscale, np.array([e1[0].sq[j+1][0], e1[0].sq[j+1][1]])*DPscale, 'black')

    #삭제되어야 할 것은 삭제
    k = 0
    while k < len(Entities):
        if Entities[k].willbeDisappear:
            Entities.pop(k)
        k+=1

    #dr.window.title(str(1/dt))

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime

