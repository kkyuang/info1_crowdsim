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

        #열린 노드
        openLists = [startRegion]

        #닫힌 노드
        closed = []

        closed_motherNode = {}

        #함수들 정의
        g = {}
        h = {}
        f = {}
        g[startRegion] = 0
        h[startRegion] = self.distReigon(startRegion, destReigon)
        f[startRegion] = h[startRegion]

        if not (startRegion in self.map.reigons.keys()):
            return [destReigon]

        #저장된 경로에 존재할 경우
        if (startRegion, destReigon) in self.routes:
            return self.routes[(startRegion, destReigon)]
        else:
            while openLists:
                currentNode = openLists[0]
                currentIdx = 0

                for i in range(len(openLists)):
                    if f[openLists[i]] < f[currentNode] and not(openLists[i] in closed):
                        currentNode = openLists[i]
                        currentIdx = i

                openLists.pop(currentIdx)
                closed.append(currentNode)


                #목표 노드의 부모 노드 찾아 나가기
                if currentNode == destReigon:
                    break
                        
                #새로 탐색할 노드를 자신의 자식으로 만들기
                children = self.map.reigons[currentNode].linkeds.copy()
                for i in children:
                    if currentNode in closed_motherNode:
                        if closed_motherNode[currentNode] == i:
                            continue
                    closed_motherNode[i] = currentNode

                for child in children:
                    if child in closed:
                        continue
                    g[child] = g[currentNode] + self.distReigon(currentNode, child)
                    h[child] = self.distReigon(child, destReigon)
                    f[child] = g[child] + h[child] + self.map.regionDensity(child)
                    if len([openNode for openNode in openLists 
                           if child == openNode and g[child] > g[openNode]]) > 0:
                        continue
                        
                    openLists.append(child)
            
            #print("end")
            #print(startRegion)
            #print(closed)
            #print(closed_motherNode)
            #print(destReigon)

            #목적지의 부모가 정해지지 않으면?
            if not(destReigon in closed_motherNode):
                print(startRegion)
                print(destination)
                return 'error'

            sequence = [destReigon]

            while True: #시작 노드가 나올 때까지 반복
                if closed_motherNode[sequence[len(sequence) - 1]] in sequence:
                    break
                sequence.append(closed_motherNode[sequence[len(sequence) - 1]])
                if sequence[len(sequence) - 1] == startRegion:
                    break

            
            sequence.reverse()
            self.routes[(startRegion, destReigon)] = sequence
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
                
            
