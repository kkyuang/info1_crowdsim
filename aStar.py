import math
import numpy as np
from Map import Map 
from Map import Reigon

#A* 알고리즘
#입력: 맵, 현재 위치, 목적지

class aStar:
    def __init__(self, map: Map):
        self.map = map
        #이미 계산된 경로들을 저장
        self.routes = {}
        pass

    #현재 위치한 구역
    def getReigon(self, position):
        myReigonStart = np.array([0, 0])
        myReigonEnd = np.array([0, 0])
        for i in range(len(self.map.vertical_lines)-1):
            if self.map.vertical_lines[i] <= position[0] and position[0] < self.map.vertical_lines[i + 1]:
                myReigonStart[0] = self.map.vertical_lines[i]
                myReigonEnd[0] = self.map.vertical_lines[i+1]

        for i in range(len(self.map.horizontal_lines)-1):
            if self.map.horizontal_lines[i] <= position[1] and position[1] < self.map.horizontal_lines[i + 1]:
                myReigonStart[1] = self.map.horizontal_lines[i]
                myReigonEnd[1] = self.map.horizontal_lines[i+1]

        return self.map.getReigonID(myReigonStart, myReigonEnd)
    
    #구역 간 거리 매기기
    def distReigon(self, start, end):
        dest = (start[0] - end[0])**2 + (start[1] - end[1]) ** 2
        return math.sqrt(dest)

    #길찾기 함수
    def findRoute(self, startpos, destination):
        #시작, 목적지
        startRegion = self.getReigon(startpos)
        destReigon = self.getReigon(destination)

        #닫힌 노드
        closed = [startRegion]

        #저장된 경로에 존재할 경우
        if (startRegion, destReigon) in self.routes:
            return self.routes[(startRegion, destReigon)]
        else:
            #시작 구역에서 탐색 시작하기

            #탐색중인 노드
            searching = self.map.reigons[startRegion].linkeds
            print(destReigon)

            #목표 노드가 나올 때까지 반복
            while True:
                #연결된 노드들의 cost 함수 매기기
                costs = [float("inf") for i in range(len(searching))]
                for i in range(len(searching)):
                    if not (searching[i] in closed):
                        g = self.distReigon(startRegion, searching[i])
                        h = self.distReigon(searching[i], destReigon)
                        costs[i] = g + h

                #최소 노드 확인 후 closed에 추가 및 탐색중인 노드 범위 넓히기
                minV = costs.index(min(costs))
                closed.append(searching[minV])
                searching += self.map.reigons[searching[minV]].linkeds

                #만약 새로 추가된 최소노드가 목표 노드라면?
                if searching[minV] == destReigon:
                    break

            #목표 노드의 부모 노드 찾아 나가기
            sequence = [destReigon]
            while True: #시작 노드가 나올 때까지 반복
                nowLinks = self.map.reigons[searching[minV]].linkeds
                for i in nowLinks:
                    if i in closed:
                        sequence.append(i)
                
                if sequence[len(sequence) - 1] == startRegion:
                    break

            return sequence
                
            
