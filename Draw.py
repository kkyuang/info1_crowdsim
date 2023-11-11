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
        self.window.resizable(True, True)# 버튼 만들기 + 옵션 설정


        #캔버스 정의
        self.canvas = tkinter.Canvas(self.window, width=screensize[0], height=screensize[1], bd=2)
        self.position_label = tkinter.Label(self.window, text="마우스 좌표:")
    def _from_rgb(self, r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
            
        r = int(r)
        g = int(g)
        b = int(b)

        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0

        return f'#{r:02x}{g:02x}{b:02x}'
    #버튼 생성
    def makeBtn(self, label, cmd):

        btn = tkinter.Button(self.window,
        text = label,
        background = 'white')
 
        # 버튼 옵션설정
        btn.config(width = 5, height = 2, command=cmd)
 
        # 버튼 배치하기
        btn.pack()

        return btn
    
    #클릭 이벤트 생성
    def clickEvent(self, event):
        self.canvas.bind("<Button-1>", event)
    
    #마우스 좌표 획득
    def mousePos(self):
        x, y = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(), self.canvas.winfo_pointery()- self.canvas.winfo_rooty()
        return (x, y)


    #텍스트 좌표 안내
    def coordinateText(self, DPscale):
        x, y = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(), self.canvas.winfo_pointery()- self.canvas.winfo_rooty()
        self.position_label.config(text=f"현재 좌표: x={round(x/DPscale, 2)}, y={round(y/DPscale, 2)}")
        self.position_label.pack()

    #원 그리기
    def DrawCircle(self, center, radius, color):
        self.canvas.create_oval(center[0] - radius, center[1] - radius,  center[0] + radius, center[1] + radius, fill=color)
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
        


