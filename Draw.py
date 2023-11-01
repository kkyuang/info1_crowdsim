import tkinter
from Entity import Entity
import numpy as np
import time


#GUI 화면 클래스(스크린사이즈, )
class Drawer:
    def __init__(self, screensize):
        #윈도우 노출 코드
        self.window=tkinter.Tk()

        self.window.title("HELLO")
        self.window.geometry(str(screensize[0]) + "x" + str(screensize[1]) + "+100+100")
        self.window.resizable(False, False)

        #캔버스 정의
        self.canvas = tkinter.Canvas(self.window, width=screensize[0], height=screensize[1], bd=2)

    def DrawCircle(self, center, radius):
        self.canvas.create_oval(center[0] - radius/2, center[1] - radius/2,  center[0] + radius/2, center[1] + radius/2, fill='red')
        self.canvas.pack()

    def windowShow(self):
        self.window.mainloop()

    def canvasClear(self):
        self.canvas.delete("all")

    def windowUpdate(self):
        self.window.update()
        self.window.update_idletasks()


dr = Drawer(np.array([640, 480]))        

dt = 0

startPosition = 0
while 1:
    #프레임 체크를 위한 시작 시간
    startTime = time.time()
    #화면 초기화
    dr.canvasClear()

    ##메인 프로그램 작성
    startPosition += dt * 20

    dr.DrawCircle(np.array([startPosition, 231]), 19)
    dr.window.title(str(dt))

    dr.windowUpdate()


    #프레임 체크를 위한 루프의 마지막 시간
    endTime = time.time()
    dt = endTime - startTime