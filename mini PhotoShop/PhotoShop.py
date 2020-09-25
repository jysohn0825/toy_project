## 라이브러리 선언부
from tkinter.filedialog import *
from tkinter.simpledialog import *
import math
import cv2
import numpy as np

## 함수 선언부
# 메모리 할당
def malloc(h, w, value=255) :
    retMemory = [ [ value for _ in range(w)]  for _ in range(h) ]
    return retMemory
# 파일 열기
def openFile() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    ## 파일 선택하기
    filename = askopenfilename(parent=window, filetypes=(('Color 파일', '*.jpg;*.png;*.bmp;*.tif'), ('All File', '*.*')))
    if filename == None:
        return
    ## (중요!) 입력이미지의 높이와 폭 알아내기
    cvInImage = cv2.imread(filename)
    inH = cvInImage.shape[0]
    inW = cvInImage.shape[1]
    ## 입력이미지용 메모리 할당
    inImage = []
    for _ in range(RGB) :
        inImage.append(malloc(inH, inW))
    ## 파일 --> 메모리 로딩
    for i in range(inH):
        for k in range(inW):
            inImage[R][i][k] = cvInImage.item(i, k ,B)
            inImage[G][i][k] = cvInImage.item(i, k, G)
            inImage[B][i][k] = cvInImage.item(i, k, R)
    outH = inH;
    outW = inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                outImage[rgb][i][k] = inImage[rgb][i][k]
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    displayImage()
# 파일 저장
def saveFile() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == None or filename == '' :
        return
    saveCvPhoto = np.zeros((outH, outW, 3), np.uint8)
    for i in range(outH) :
        for k in range(outW) :
            tup = tuple(([outImage[B][i][k],outImage[G][i][k],outImage[R][i][k]]))
            saveCvPhoto[i,k] = tup
    saveFp = asksaveasfile(parent=window, mode='wb',defaultextension='.', filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    cv2.imwrite(saveFp.name, saveCvPhoto)
# 이미지 보여주기
def displayImage() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    window.geometry(str(outW) + 'x' + str(outH+20))
    if canvas != None:
        canvas.destroy()
    canvas = Canvas(window, height=outH, width=outW)
    paper = PhotoImage(height=outH, width=outW)
    canvas.create_image((outW / 2, outH / 2), image=paper, state='normal')
    # 메모리에서 처리한 후, 한방에 화면에 보이기 --> 완전 빠름
    rgbString = ""
    for i in range(outH):
        tmpString = ""  # 각 줄
        for k in range(outW):
            r = outImage[R][i][k]
            g = outImage[G][i][k]
            b = outImage[B][i][k]
            tmpString += "#%02x%02x%02x " % (r, g, b)
        rgbString += '{' + tmpString + '} '
    paper.put(rgbString)
    canvas.pack()
    status.configure(text='이미지정보:' + str(outH) + 'x' + str(outW) + '      ' + filename)
# 그레이 스케일링
def changeGray() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    gray = []
    for _ in range(RGB):
        gray.append(malloc(outH, outW))
    for i in range(inH):
        for j in range(inW):
            ### 흑백 변환
            avg = int((inImage[R][i][j] + inImage[G][i][j] + inImage[B][i][j]) / 3)
            gray[R][i][j] = gray[G][i][j] = gray[B][i][j] = avg
    return gray
# 키보드 이벤트
def keyEvent(event):
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage, cancel
    key = chr(event.keycode)
    if key == "Z":
        if cancel == True:
            outImage = []
            outH = np.shape(cancelImage)[1]
            outW = np.shape(cancelImage)[2]
            for _ in range(RGB):
                outImage.append(malloc(outH, outW))
            for c in range(RGB):
                for i in range(outH):
                    for j in range(outW):
                        outImage[c][i][j] = cancelImage[c][i][j]
            cancel = False
            displayImage()
        else :
            outImage = []
            outH = np.shape(notCancelImage)[1]
            outW = np.shape(notCancelImage)[2]
            for _ in range(RGB):
                outImage.append(malloc(outH, outW))
            for c in range(RGB):
                for i in range(outH):
                    for j in range(outW):
                        outImage[c][i][j] = notCancelImage[c][i][j]
            cancel = True
            displayImage()


### 영상처리 함수
# 동일영상 알고리즘
def equalColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB) :
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    ### 진짜 영상처리 알고리즘 ###
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                outImage[rgb][i][k] = notCancelImage[c][i][j] = inImage[rgb][i][k]
    displayImage()
# 밝게하기 알고리즘
def addColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None :
        return
    ## 출력이미지의 높이, 폭을 결정
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    ### 진짜 영상처리 알고리즘 ###
    value = askinteger("","밝게하기 값")
    for c in range(RGB) :
        for i in range(inH) :
            for j in range(inW) :
                ### 밝게 하기 (오버플로우 처리)
                out = inImage[c][i][j] + value
                if out > 255:
                    outImage[c][i][j] = notCancelImage[c][i][j] =255
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] =out
    displayImage()
# 어둡게하기 알고리즘
def subColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None :
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    value = askinteger("","어둡게하기 값")
    if value == None:
        return
    for c in range(RGB) :
        for i in range(inH) :
            for j in range(inW) :
                out = inImage[c][i][j] - value
                if out < 0:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = out
    displayImage()
# 이진수변환(127 기준) 알고리즘
def binary127Color() : # 이진수변환 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    gray = changeGray() # 이진수 변환을 위한 컬러->흑백화
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                if gray[R][i][j] > 127 : # gray 리스트는 흑백화 했으므로 R,G,B 상관 없이 색이 같음
                    outImage[c][i][j] =  notCancelImage[c][i][j] = 255
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
    displayImage()
# 이진수변환(평균값 기준) 알고리즘
def binaryAvgColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    gray = changeGray()
    # 평균 구하기
    sum = 0
    for i in range(inH):
        for j in range(inW):
            sum += gray[R][i][j] # gray 리스트는 흑백화 했으므로 R,G,B 상관 없이 색이 같아서 1회만 더함
    avg = int(sum/(inH*inW))
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                if gray[R][i][j] > avg : # gray 리스트는 흑백화 했으므로 R,G,B 상관 없이 색이 같음
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
    displayImage()
# 이진수변환(중위값 기준) 알고리즘
def binaryMidColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    outH, outW = inH, inW
    gray = changeGray()
    # 중위값 구하기
    temp = []
    for i in range(inH):
        for j in range(inW):
            temp.append(gray[R][i][j])  # gray 리스트는 흑백화 했으므로 R,G,B 상관 없이 색이 같아서 1회만 더함
    temp.sort()
    mid = temp[int((inH*inW)/2)]
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                if gray[R][i][j] > mid:  # gray 리스트는 흑백화 했으므로 R,G,B 상관 없이 색이 같음
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
    displayImage()
# 이진수변환(범위 기준) 알고리즘
def binaryRangeColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    gray = changeGray()
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    p1 = askinteger("", "값 :")
    p2 = askinteger("", "값 :")
    if p1 == None and p2 == None:
        return
    if p1 > p2:
        p1, p2 = p2, p1
    for c in range(RGB):
        for i in range(outH) :
            for j in range(outW) :
                if p1 < gray[R][i][j] < p2:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                else :
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
    displayImage()
# 영상 반전 알고리즘
def reverseColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                # 영상 반전
                outImage[c][i][j] = notCancelImage[c][i][j] = 255 - inImage[c][i][j]
    displayImage()
# 포스터라이징 알고리즘
def posterizingColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    value = askinteger("", "경계값 :", minvalue=1, maxvalue=255)
    if value == None:
        return
    temp = int(outW / value)
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                for k in range(temp, outW, temp):
                    if k <= inImage[c][i][j] < k+temp:
                        if k + temp > 255:
                          outImage[c][i][j] = notCancelImage[c][i][j] = 255
                        else:
                          outImage[c][i][j] = notCancelImage[c][i][j] = k+temp
                        break
    displayImage()
# 감마변환 알고리즘
def gammaColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    value = askfloat("", "감마값 :")
    if value == None:
        return
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                v = inImage[c][i][j] ** (1/value)
                if  v > 255:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                elif v < 0:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = int(v)
    displayImage()
# 파라볼릭 캡 알고리즘
def parabolicCapColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                v = 255 - 255.0 * ((inImage[c][i][j]/128.0 - 1.0)**2)
                if  v > 255:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                elif v < 0:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = int(v)
    displayImage()
# 파라볼릭 캡 알고리즘
def parabolicCupColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                v = 255.0 * ((inImage[c][i][j]/128.0 - 1.0)**2)
                if  v > 255:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                elif v < 0:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = int(v)
    displayImage()
# 미러링(좌우) 알고리즘
def mirrorRightLeftColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    outH, outW = inH, inW
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                outImage[c][i][j] = notCancelImage[c][i][j] = inImage[c][i][outW - j - 1]
    displayImage()
# 미러링(상하) 알고리즘
def mirrorUpDownColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    outH, outW = inH, inW
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                outImage[c][i][j] = notCancelImage[c][i][j] = inImage[c][outH - i - 1][j]
    displayImage()
# 이동 알고리즘
def moveColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    dx = askinteger("", "움직일 x값 :")
    dy = askinteger("", "움직일 y값 :")
    if dx == None and dy == None:
        return
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                if 0 <= i + dx < outH and 0 <= j + dy < outW:
                    outImage[c][i + dx][j + dy] = notCancelImage[c][i][j] = inImage[c][i][j]
    displayImage()
# 회전 알고리즘
def rotateColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    value = askinteger("", "회전 각도 :", minvalue=0, maxvalue=360)
    if value == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    # for c in range(RGB):
    #     for i in range(outH):
    #         for j in range(outW):
    #             cancelImage[c][i][j] = outImage[c][i][j]
    radian = value * math.pi / 180
    reverseRadian = (90 - value) * math.pi / 180
    outH = int(inH * math.cos(radian) + inW * math.cos(reverseRadian))
    outW = int(inH * math.cos(reverseRadian) + inW * math.cos(radian))
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        # notCancelImage.append(malloc(outH, outW))
    tmpImage = []
    for _ in range(RGB):
        tmpImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpImage[c][i+int((outH-inH)/2)][j+int((outW-inW)/2)] = inImage[c][i][j]
    centerX = outH//2
    centerY = outW//2
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                xd = int(math.cos(radian) * (i - centerX) - math.sin(radian) * (j - centerY) + centerX)
                yd = int(math.sin(radian) * (i - centerX) + math.cos(radian) * (j - centerY) + centerY)
                if 0 <= xd < outH and 0 <= yd < outW:
                    outImage[c][i][j] = tmpImage[c][xd][yd]  # = notCancelImage[c][i][j] = tmpImage[c][xd][yd]
    displayImage()
# 확대 알고리즘
def expandColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    value = askinteger("", "확대 배율값 :")
    if value == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    # for c in range(RGB):
    #     for i in range(outH):
    #         for j in range(outW):
    #             cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH * value, inW * value
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        # notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                outImage[c][i][j] = inImage[c][int(i/value)-1][int(j/value)-1] # = notCancelImage[c][i][j] = inImage[c][int(i/value)-1][int(j/value)-1]
    displayImage()
# 축소 알고리즘
def reductColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    value = askinteger("", "축소 배율값 :")
    if value == None:
        return
    # for _ in range(RGB):
    #     cancelImage.append(malloc(outH, outW))
    # for c in range(RGB):
    #     for i in range(outH):
    #         for j in range(outW):
    #             cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = int(inH/value), int(inW/value)
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                temp = 0
                for k in range(value):
                    for l in range(value):
                        temp += inImage[c][i*value+k][j*value+l]
                outImage[c][i][j] = int(temp / (value * value)) # = notCancelImage[c][i][j] = int(temp / (value * value))
    displayImage()
# 블러 알고리즘
def blurColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    value = askinteger("", "블러값 :")
    if value == None:
        return
    tmpInImage = []
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+value-1, outW+value-1,127))
    mask = []
    for i in range(value):
        temp = []
        for j in range(value):
            temp.append(1/(value*value))
        mask.append(temp)
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i+1][j+1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1,outH+1):
            for j in range(1,outW+1):
                sum = 0.0 # mask 값들의 합이 0이 아닐 경우 0으로 세팅
                for m in range(value):
                    for n in range(value):
                        sum += tmpInImage[c][i-1+m][j-1+n] * mask[m][n]
                outImage[c][i-1][j-1] = notCancelImage[c][i-1][j-1] = int(sum)
    displayImage()
# 샤프닝 알고리즘
def sharpColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    tmpInImage = []
    nSIZE = 3
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+nSIZE-1, inW+nSIZE-1,127))
    mask = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i + 1][j + 1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1, outH + 1):
            for j in range(1, outW + 1):
                sum = 0.0  # mask 값들의 합이 0이 아닐 경우 0으로 세팅
                for m in range(nSIZE):
                    for n in range(nSIZE):
                        sum += tmpInImage[c][i - 1 + m][j - 1 + n] * mask[m][n]
                if sum < 0:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 0
                elif sum > 255:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 255
                else:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = int(sum)
    displayImage()
# 엠보싱 알고리즘
def embossColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    tmpInImage = []
    nSIZE = 3
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+nSIZE-1, inW+nSIZE-1,127))
    mask = [[-1, 0, 0], [0, 0, 0], [0, 0, 1]]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i + 1][j + 1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1, outH + 1):
            for j in range(1, outW + 1):
                sum = 128.0  # mask 값들의 합이 0일 경우 128로 세팅
                for m in range(nSIZE):
                    for n in range(nSIZE):
                        sum += tmpInImage[c][i - 1 + m][j - 1 + n] * mask[m][n]
                if sum < 0:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 0
                elif sum > 255:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 255
                else:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = int(sum)
    displayImage()
# 경계값 추출 알고리즘
def boundaryColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    tmpInImage = []
    nSIZE = 3
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+nSIZE-1, inW+nSIZE-1,127))
    mask = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i + 1][j + 1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1, outH + 1):
            for j in range(1, outW + 1):
                sum = 128.0  # mask 값들의 합이 0일 경우 128로 세팅
                for m in range(nSIZE):
                    for n in range(nSIZE):
                        sum += tmpInImage[c][i - 1 + m][j - 1 + n] * mask[m][n]
                if sum < 0:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 0
                elif sum > 255:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 255
                else:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = int(sum)
    displayImage()
# 유사연산자 알고리즘
def simOpColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    tmpInImage = []
    nSIZE = 3
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+nSIZE-1, inW+nSIZE-1,127))
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i + 1][j + 1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1, outH + 1):
            for j in range(1, outW + 1):
                temp = []
                for m in range(-1,2):
                    for n in range(-1,2):
                        temp.append(abs(tmpInImage[c][i][j] - tmpInImage[c][i+m][j+n]))
                outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = max(temp)
    displayImage()
# 차연산자 알고리즘
def subOpColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    tmpInImage = []
    nSIZE = 3
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+nSIZE-1, inW+nSIZE-1,127))
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i + 1][j + 1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1, outH + 1):
            for j in range(1, outW + 1):
                temp = [abs(tmpInImage[c][i-1][j-1] - tmpInImage[c][i+1][j+1]),
                        abs(tmpInImage[c][i-1][j+1] - tmpInImage[c][i+1][j-1]),
                        abs(tmpInImage[c][i-1][j] - tmpInImage[c][i+1][j]),
                        abs(tmpInImage[c][i][j-1] - tmpInImage[c][i][j+1])]
                outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = int(max(temp))
    displayImage()
# LoG 알고리즘
def logColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    tmpInImage = []
    nSIZE = 5
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+nSIZE-1, inW+nSIZE-1,127))
    mask = [[0,0,-1,0,0],
            [0,-1,-2,-1,0],
            [-1,-2,16,-2,-1],
            [0,-1,-2,-1,0],
            [0,0,-1,0,0]]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i + 1][j + 1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1, outH + 1):
            for j in range(1, outW + 1):
                sum = 128.0  # mask 값들의 합이 0이 아닐 경우 0으로 세팅
                for m in range(nSIZE):
                    for n in range(nSIZE):
                        sum += tmpInImage[c][i - 1 + m][j - 1 + n] * mask[m][n]
                if sum < 0:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 0
                elif sum > 255:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 255
                else:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = int(sum)
    displayImage()
# DoG 알고리즘
def dogColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    tmpInImage = []
    nSIZE = 7
    for _ in range(RGB):
        tmpInImage.append(malloc(inH + nSIZE - 1, inW + nSIZE - 1, 127))
    mask = [[0, 0, -1, -1, -1, 0, 0],
            [0, -2, -3, -3, -3, -2, 0],
            [-1, -3, 5, 5, 5, -3, -1],
            [-1, -3, 5, 16, 5, -3, -1],
            [-1, -3, 5, 5, 5, -3, -1],
            [0, -2, -3, -3, -3, -2, 0],
            [0, 0, -1, -1, -1, 0, 0]]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                tmpInImage[c][i + 1][j + 1] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(1, outH + 1):
            for j in range(1, outW + 1):
                sum = 128.0  # mask 값들의 합이 0이 아닐 경우 0으로 세팅
                for m in range(nSIZE):
                    for n in range(nSIZE):
                        sum += tmpInImage[c][i - 1 + m][j - 1 + n] * mask[m][n]
                if sum < 0:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 0
                elif sum > 255:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = 255
                else:
                    outImage[c][i - 1][j - 1] = notCancelImage[c][i-1][j-1] = int(sum)
    displayImage()
# 스트래칭 알고리즘
def stretchColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    low = [inImage[R][0][0], inImage[G][0][0], inImage[B][0][0]]
    high = [inImage[R][0][0], inImage[G][0][0], inImage[B][0][0]]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                if low[c] > inImage[c][i][j]:
                    low[c] = inImage[c][i][j]
                elif high[c] < inImage[c][i][j]:
                    high[c] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                out = (inImage[c][i][j] - low[c])/(high[c] - low[c]) * 255.0
                if out > 255:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                elif out < 0:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = int(out)
    displayImage()
# 엔드인 탐색 알고리즘
def endInSearchColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    ADD = 32
    low = [inImage[R][0][0]+ADD, inImage[G][0][0]+ADD, inImage[B][0][0]+ADD]
    high = [inImage[R][0][0]+ADD, inImage[G][0][0]+ADD, inImage[B][0][0]+ADD]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                if low[c] > inImage[c][i][j]:
                    low[c] = inImage[c][i][j]
                elif high[c] < inImage[c][i][j]:
                    high[c] = inImage[c][i][j]
    for c in range(RGB):
        for i in range(inH):
            for j in range(inW):
                out = (inImage[c][i][j] - low[c]) / (high[c] - low[c]) * 255.0
                if out > 255:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 255
                elif out < 0:
                    outImage[c][i][j] = notCancelImage[c][i][j] = 0
                else:
                    outImage[c][i][j] = notCancelImage[c][i][j] = int(out)
    displayImage()
# 평활화 알고리즘
def equalizedColor() :
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename, cvInImage, cvOutImage, cancelImage, notCancelImage
    if filename == '' or filename == None:
        return
    for _ in range(RGB):
        cancelImage.append(malloc(outH, outW))
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                cancelImage[c][i][j] = outImage[c][i][j]
    outH, outW = inH, inW
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
        notCancelImage.append(malloc(outH, outW))
    histogram = [ 0  for _ in range(256)]
    for i in range(inH):
        for j in range(inW):
            histogram[int((inImage[R][i][j]+inImage[G][i][j]+inImage[B][i][j])/3)] += 1
    sumHistogram = [0 for _ in range(256)]
    sumHistogram[0] = histogram[0]
    for i in range(1,256):
        sumHistogram[i] = histogram[i] + sumHistogram[i-1]
    for c in range(RGB):
        for i in range(outH):
            for j in range(outW):
                outImage[c][i][j] = notCancelImage[c][i][j] = int(sumHistogram[inImage[c][i][j]] * (1/(inH*inW)) * 255)
    displayImage()

## 전역 변수부
window, canvas, paper = None, None, None
inImage, outImage, cancelImage, notCancelImage = [], [], [], []
cvInImage, cvOutImage = None, None
inH, inW, outH, outW = [0] * 4
filename = ''
RGB, R, G, B = 3, 0, 1, 2
cancel = True

## 메인 코드부
if __name__ == '__main__' :
    window = Tk()
    window.bind("<Key>", keyEvent)
    window.title('컬러 영상처리')
    window.geometry('512x512')
    window.resizable(height=False, width=False)
    status = Label(window, text="이미지 정보", bd = 1, relief = SUNKEN, anchor = W)
    status.pack(side = BOTTOM, fill = X)

    ### 메뉴 만들기 ###
    mainMenu = Menu(window)
    window.configure(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_command(label="열기", command=openFile)
    fileMenu.add_command(label="저장", command=saveFile)
    fileMenu.add_separator()
    fileMenu.add_command(label="닫기")

    pixelMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리", menu=pixelMenu)
    pixelMenu.add_command(label="동일영상", command=equalColor)
    pixelMenu.add_command(label="밝게", command=addColor)
    pixelMenu.add_command(label="어둡게", command=subColor)
    pixelMenu.add_command(label="이진화(127)", command=binary127Color)
    pixelMenu.add_command(label="이진화(평균값)", command=binaryAvgColor)
    pixelMenu.add_command(label="이진화(중위수)", command=binaryMidColor)
    pixelMenu.add_command(label="범위강조변환", command=binaryRangeColor)
    pixelMenu.add_command(label="영상반전", command=reverseColor)
    pixelMenu.add_command(label="포스터라이징", command=posterizingColor)
    pixelMenu.add_command(label="감마", command=gammaColor)
    pixelMenu.add_command(label="파라볼라(cap)", command=parabolicCapColor)
    pixelMenu.add_command(label="파라볼라(cup)", command=parabolicCupColor)

    geometryMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="기하학 처리", menu=geometryMenu)
    geometryMenu.add_command(label="미러링(좌우)", command=mirrorRightLeftColor)
    geometryMenu.add_command(label="미러링(상하)", command=mirrorUpDownColor)
    geometryMenu.add_command(label="이동", command=moveColor)
    geometryMenu.add_command(label="회전", command=rotateColor)
    geometryMenu.add_command(label="확대", command=expandColor)
    geometryMenu.add_command(label="축소", command=reductColor)

    processMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="화소영역 처리", menu=processMenu)
    processMenu.add_command(label="블러링", command=blurColor)
    processMenu.add_command(label="샤프닝", command=sharpColor)
    processMenu.add_command(label="엠보싱", command=embossColor)
    processMenu.add_command(label="경계추출", command=boundaryColor)
    processMenu.add_command(label="유사연산자", command=simOpColor)
    processMenu.add_command(label="차연산자", command=subOpColor)
    processMenu.add_command(label="LoG", command=logColor)
    processMenu.add_command(label="DoG", command=dogColor)

    histogramMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="히스토그램", menu=histogramMenu)
    histogramMenu.add_command(label="스트래칭", command=stretchColor)
    histogramMenu.add_command(label="앤드인탐색", command=endInSearchColor)
    histogramMenu.add_command(label="평활화", command=equalizedColor)

    window.mainloop()