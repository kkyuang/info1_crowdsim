import tkinter
from Entity import Entity
import numpy as np
import time


#GUI 화면 클래스(스크린사이즈, )
class Drawer:
    def __init__(self, screensize):
        #윈도우 노출 코드
        self.window=tkinter.Tk()
        self.screensize = screensize

        self.window.title("군중 시뮬레이션")
        self.window.geometry(str(screensize[0]) + "x" + str(screensize[1]) + "+100+100")
        self.window.resizable(False, False)# 버튼 만들기 + 옵션 설정


        #캔버스 정의
        self.canvas = tkinter.Canvas(self.window, width=screensize[0], height=screensize[1], bd=2)
        self.position_label = tkinter.Label(self.window, text="마우스 좌표:")

    #버튼 생성
    def makeBtn(self, label):

        btn = tkinter.Button(self.window,
        text = label,
        background = 'white')
 
        # 버튼 옵션설정
        btn.config(width = 5, height = 2)
 
        # 버튼 배치하기
        btn.pack()

    #텍스트 좌표 안내
    def coordinateText(self):
        x, y = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(), self.canvas.winfo_pointery()- self.canvas.winfo_rooty()
        self.position_label.config(text=f"현재 좌표: x={x/10}, y={y/10}")
        self.position_label.pack()

    #원 그리기
    def DrawCircle(self, center, radius, color):
        self.canvas.create_oval(center[0] - radius/2, center[1] - radius/2,  center[0] + radius/2, center[1] + radius/2, fill=color)
        self.canvas.pack()

    def DrawRectangle(self, start, end, color):
        self.canvas.create_rectangle(start[0], start[1], end[0], end[1], fill=color)
        self.canvas.pack()

    def DrawRectangle2(self, start, end, color):
        self.canvas.create_rectangle(start[0], start[1], end[0], end[1], outline=color)
        self.canvas.pack()

    def DrawLine(self, start, end, color):
        self.canvas.create_line(start[0], start[1], end[0], end[1], fill=color, width=1)
        self.canvas.pack()

    #창 띄우기(정적)
    def windowShow(self):
        self.window.mainloop()

    #캔버스 초기화
    def canvasClear(self):
        self.canvas.delete("all")

    #창 새로고침
    def windowUpdate(self):
        self.window.update()
        self.window.update_idletasks()

    #화면 좌표로 변환
    #def convertPos(self, position, originPos, onemeterpx):
        


