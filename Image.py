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