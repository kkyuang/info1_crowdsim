import tkinter
import tkinter.font
import os
from tkinter import filedialog

# 시작 함수
def start():
    print("start")
    window.destroy()
    os.system("python main.py")


# 파일을 불러오는 함수
def fileload():
    file = filedialog.askopenfilenames(initialdir="/", title = "파일 불러오기", \
                                        filetypes = (("jpg 파일","*jpg"), ("png 파일","*png"), \
                                                     ("모든 파일", "*.*")))
    label_info.config(text = file)
    if(file != ''):
        print("file loaded")
    else:
        label_info.config(text = "None")

window = tkinter.Tk()

# tkinter 윈도우 설정
window.title("Lobby")
window.geometry ("640x400+100+100")
window.resizable(False, False)

# 디자인 폰트
font_1 = tkinter.font.Font(family = "Comic Sans MS", size = 24)
font_2 = tkinter.font.Font(family = "나눔고딕 ExtraBold", size = 10)

label_title = tkinter.Label(window, text = "Info1_Crowd", font = font_1)
label_title.pack(side = "top")

# 파일 불러오기 버튼
button_fileload = tkinter.Button(window, text = "파일 불러오기", overrelief = "solid", command = fileload, \
                        font = font_2)
button_fileload.pack()

# 파일 정보 라벨
label_info = tkinter.Label(window, text = "None", font = font_2)
label_info.pack()

# 시뮬레이션 시작 버튼
button_start = tkinter.Button(window, text = "시작!", overrelief = "solid", command = start, \
                        font = font_2)
button_start.pack()

window.mainloop()