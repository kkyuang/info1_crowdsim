import tkinter
import tkinter.font
import os
from tkinter import filedialog
from PIL import Image
import pickle

# 시작 함수
def start():
    print("start")
    window.destroy()
    os.system("python main.py")


# 파일을 불러오는 함수
def fileload():
    file = filedialog.askopenfilenames(initialdir="./image", title = "파일 불러오기", \
                                        filetypes = (("jpg 파일","*jpg"), ("png 파일","*png"), ("bmp 파일","*bmp"), \
                                                     ("모든 파일", "*.*")))

    label_info.config(text = file)
    if(file != ''):

        im = Image.open(file[0])

        print(im.size)

        x = im.size[0]#int(input("원하는 가로 길이? "))
        y = im.size[1]#int(input("원하는 세로 길이? "))

        #resize_image2 = im.resize((int(im.size[0]/x), int(im.size[1]/y)))
        resize_image2 = im.resize((x, y), Image.Resampling.BOX )

        rgb_im = resize_image2.convert('RGB')
        resize_image2.show()

        arr = [[0 for j in range(y)] for i in range(x)]

        for i in range(x) :
            for j in range(y) :
                r, g, b = rgb_im.getpixel((i, j))

                print(r, g, b)
                if (0<= r and r <= 50) and (0<= g and g <= 50)and (0<= b and b <= 50):
                    arr[i][j]=1
                elif r==0 and g==255 and b==0 : 
                    arr[i][j]=2
                elif r==0 and g==0 and (120<= b and b <= 140) : 
                    arr[i][j]=3
                elif r==0 and g==0 and (240<= b and b <= 255) : 
                    arr[i][j]=4
                elif (120<= r and r <= 140) and g==0 and b==0 : 
                    arr[i][j]=5
                elif (240<= r and r <= 255) and g==0 and b==0 : 
                    arr[i][j]=6
                else :
                    arr[i][j]=0
                r=0
                g=0
                b=0

        for i in range(x) :
            for j in range(y) :
                print(arr[i][j],end=" ")
            print()


        #맵 요소 타입
        #1: 장애물(검은색 벽) -> #000000
        #2: 탈출구 -> #00FF00
        #3: 군중그룹 1의 시작구역 -> #000080
        #4: 군중그룹 1의 목표구역 -> #0000FF
        #5: 군중그룹 2의 시작구역 -> #800000
        #6: 군중그룹 2의 목표구역 -> #FF0000

        MapElements = {'size': (x, y), 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}

        #이중for문을 통한 순차탐색
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                #비어있지 않은 공간(장애물 등)이 나오면?
                if arr[i][j] != 0:
                    mapType = arr[i][j]

                    #왼쪽 직사각형 높이
                    #leftHeight = 0
                    #바로 아래로 탐색
                    #for k in range(i, len(arr)):
                    #    #탐색 시작점과 다른 타일이 나오면 탈출
                    #    if arr[k][j] != mapType:
                    #        break
                    #   leftHeight+=1

                    #직사각형의 너비
                    width = 0
                    #오른쪽으로 탐색
                    for k in range(j, len(arr[i])):
                        #탐색 시작점과 다른 타일이 나오면 탈출
                        if arr[i][k] != mapType:
                            break
                        width+=1

                    height = 0

                    for k in range(i, len(arr)):
                        superBreak = False
                        for l in range(j, j + width):
                            if arr[k][l] != mapType:
                                superBreak = True
                        if superBreak:
                            break
                        height += 1

                    #오른쪽 직사각형 높이
                    rightHeight = 0
                    #바로 아래로 탐색
                    for k in range(i, len(arr)):
                        #탐색 시작점과 다른 타일이 나오면 탈출
                        if arr[k][j + width - 1] != mapType:
                            break
                        rightHeight+=1

                    #왼쪽과 오른쪽을 비교(더 짧은쪽을 취함)
                    #height = leftHeight if leftHeight < rightHeight else rightHeight
                    rectangle = ((i, j), (i + height, j + width))
                    MapElements[mapType].append(rectangle)

                    #새로 생성된 직사각형에서 0을 지우기
                    for i1 in range(rectangle[0][0], rectangle[1][0]):
                        for j1 in range(rectangle[0][1], rectangle[1][1]):
                            arr[i1][j1] = 0

        with open('MapTemp','wb') as fw:
            pickle.dump(MapElements, fw)
        
    else:
        label_info.config(text = "None")

window = tkinter.Tk()
# tkinter 윈도우 설정
window.title("Lobby")
window.geometry ("640x400+100+100")
window.resizable(False, False)

# 디자인 폰트
#font_1 = tkinter.font.Font(family = "Comic Sans MS", size = 24)
font_2 = tkinter.font.Font(family = "나눔고딕 ExtraBold", size = 10)

label_title = tkinter.Label(window, text = "Info1_Crowd", font = font_2)
label_title.pack(side = "top")

# 파일 불러오기 버튼
button_fileload = tkinter.Button(window, text = "파일 불러오기", overrelief = "solid", command = fileload, \
                        font = font_2)
button_fileload.pack()

# 파일 미리보기 라벨
label_image = tkinter.Label(window)
label_image.pack()

# 파일 정보 라벨
label_info = tkinter.Label(window, text = "None", font = font_2)
label_info.pack()

# 시뮬레이션 시작 버튼
button_start = tkinter.Button(window, text = "시작!", overrelief = "solid", command = start, \
                        font = font_2)
button_start.pack()

window.mainloop()