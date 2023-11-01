import tkinter
from Entity import Entity
import numpy as np
import time

##윈도우 노출 코드
window=tkinter.Tk()

window.title("HELLO")
window.geometry("640x400+100+100")
window.resizable(False, False)

##캔버스 정의
canvas=tkinter.Canvas(window, width=640, height=480, bd=2)

##원 그리기




entitys = [Entity(np.array([3, 2]), 0.2, np.array([600, 90])), 
           Entity(np.array([30, 50]), 0.2, np.array([600, 90])), 
           Entity(np.array([30, 80]), 0.2, np.array([600, 90])), 
           Entity(np.array([330, 50]), 0.2, np.array([600, 90])), 
           Entity(np.array([320, 20]), 0.2, np.array([600, 90])), 
           Entity(np.array([30, 90]), 0.2, np.array([600, 90]))]


class Drawer:


while(True):

    canvas.delete("all")

    for i in range(len(entitys)):
        entitys[i].move()

        arc=canvas.create_oval(entitys[i].position[0], entitys[i].position[1], entitys[i].position[0] + 30, entitys[i].position[1] + 30, fill='red')

    canvas.pack()
    window.update()
    window.update_idletasks()
    time.sleep(0.01)