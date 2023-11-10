from PIL import Image

im = Image.open("image/test.png")

im.show()

print(im.size)

x = int(input("원하는 가로 길이? "))
y = int(input("원하는 세로 길이? "))

#resize_image2 = im.resize((int(im.size[0]/x), int(im.size[1]/y)))
resize_image2 = im.resize((x, y))

rgb_im = resize_image2.convert('RGB')
resize_image2.show()

arr = [[0 for j in range(y)] for i in range(x)]

for i in range(x) :
    for j in range(y) :
        r, g, b = rgb_im.getpixel((i, j))

        print(r, g, b)
        if r==0 and g==0 and b==0 :
            arr[i][j]=1
        elif r==0 and g==255 and b==0 : 
            arr[i][j]=2
        else :
            arr[i][j]=0
        r=0
        g=0
        b=0
                    
for i in range(x) :
    for j in range(y) :
        print(arr[i][j],end=" ")
    print()


# 성준이의 직사각형 긁기 함수 ^^
for i in range(x) : # 세로(i) 순차 탐색
    for j in range(y) : # 가로(j) 순차 탐색
        if(arr[i][j]!=0): # 순차 탐색에서 배열 값이 0이 아니라면
            pos1 = [i, j] # 최초로 0이 아닌 지점 저장
            j += 1 # pos1부터 가로(j)로 긁기
            if(arr[i][j]==0) : # 긁다가 0이 아닌 지점이 끝났다면
                j -= 1 # j가 현재 0에 있으므로 1 빼기
                if(arr[i][j]!=0) : # 현재 위치의 배열 값이 0이 아니라면
                    i += 1 # 세로로 긁기
                    if(arr[i][j]==0) : # 긁다가 0이 아닌 지점이 끝났다면
                        i -= 1 # i가 현재 0에 있으므로 1 빼기
                        pos2 = [i, j] # 직사각형의 끝 지점 저장