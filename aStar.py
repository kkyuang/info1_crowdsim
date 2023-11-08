import math
import numpy as np
from Map import Map 
from Map import Reigon
import random

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
    
    def isinReigon(self, position, map:Map):
        if self.getReigon(position) in map.reigons.keys():
            return True
        else:
            return False
            
    
    #구역 간 거리 매기기
    def distReigon(self, start, end):
        dest = abs(start[0] - end[0]) + abs(start[1] - end[1])
        return dest

    #길찾기 함수
    def findRoute(self, startpos, destination):
        #시작, 목적지
        startRegion = self.getReigon(startpos)
        destReigon = self.getReigon(destination)

        #오류방지: 같은 구역일 경우
        if startRegion == destReigon:
            return [destReigon]


        #닫힌 노드
        closed = [startRegion]
        closed_motherNode = {}
        distances = {}
        distances[startRegion] = 0

        #저장된 경로에 존재할 경우
        if (startRegion, destReigon) in self.routes:
            return self.routes[(startRegion, destReigon)]
        else:
            #탐색중인 노드
            searching = self.map.reigons[startRegion].linkeds.copy()
            for i in searching:
                closed_motherNode[i] = startRegion
                distances[i] = self.distReigon(startRegion, i)

            exNode = startRegion
            #목표 노드가 나올 때까지 반복
            while True:
                #연결된 노드들의 cost 함수 매기기
                costs = [float("inf") for i in range(len(searching))]
                for i in range(len(searching)):
                    if not (searching[i] in closed):
                        distances[searching[i]] = distances[exNode] + self.distReigon(exNode, searching[i])
                        g = distances[searching[i]]
                        h = self.distReigon(searching[i], destReigon)
                        costs[i] = g + h

                #최소 노드 확인 후 closed에 추가 및 탐색중인 노드 범위 넓히기
                minV = -1
                for i in range(len(searching)):
                    if minV == -1:
                        if not (searching[i] in closed):
                            minV = i
                    if costs[i] < costs[minV] and not (searching[i] in closed):
                        minV = i

                #탐색 범위가 모두 닫힌 노드뿐임
                if minV == -1:
                    return 'error'
                        
                closed.append(searching[minV])
                for i in self.map.reigons[searching[minV]].linkeds:
                    if not (i in closed):
                        searching.append(i)
                if not searching[minV] in closed_motherNode:
                    closed_motherNode[searching[minV]] = exNode
                exNode = searching[minV]

                #만약 새로 추가된 최소노드가 목표 노드라면?
                if searching[minV] == destReigon:
                    break

            #목표 노드의 부모 노드 찾아 나가기
            sequence = [destReigon]
            while True: #시작 노드가 나올 때까지 반복
                sequence.append(closed_motherNode[sequence[len(sequence) - 1]])
                
                if sequence[len(sequence) - 1] == startRegion:
                    break

            sequence.reverse()
            return sequence
        
    #구역 내 임의 목표 목록으로 변환하는 함수
    def routeToRandom(self, map:Map, sequence):
        if sequence == 'error':
            return 'error'
        randomSeq = []
        for i in sequence:
            randomSeq.append(self.randomDestination(map.reigons[i].start, map.reigons[i].end, map))
        
        return randomSeq

    #범위 내에서 랜덤인 목적지를 설정
    def randomDestination(self, rangestart, rangeend, map):
        while True:
            dest = np.array([random.uniform(rangestart[0], rangeend[0]), random.uniform(rangestart[1], rangeend[1])])
            if self.isinReigon(dest, map):
                return dest
                
            
