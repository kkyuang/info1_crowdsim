
from PIL import Image

im = Image.open("test2.png")

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
        r, g, b = rgb_im.getpixel((j, i))

        print(r, g, b)
        if r==0 & g==0 & b==0 :
            arr[j][i]=1
        else : 
            arr[j][i]=0
        r=0
        g=0
        b=0
            
for i in range(x) :
    for j in range(y) :
        print(arr[j][i],end=" ")
    print()