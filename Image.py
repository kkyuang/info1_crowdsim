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

change = True # 긁었는지 여부를 확인하는 변수
while(change == True) :
    change = False
    for i in range(x) :
        for j in range(y) :
            if(arr[i][j]!=0):
                pos1 = (i, j) # 최초로 0이 아닌 지점 저장
                for l in range(j, y): # 옆(j)으로 긁기
                    temp = -1
                    if(temp == -1):
                        for k in range(i, x) : #아래(i)로 긁기
                            if(arr[k][l]==0) :
                                temp = k-1
                                pos2 = (temp, l)
                            else:
                                arr[k][l] = 0
                                change = True
                    
                    if(arr[k1][l]==0) :
                        pos2 = (temp, l-1) # 직사각형의 끝 지점 저장
                        change = True
                    break # for 탈출