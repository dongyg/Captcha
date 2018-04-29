#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#用画线的方法画字，画字的线与画噪声的线颜色和粗细一样，这样生成的验证码用程序识别很困难

import Image, ImageDraw, ImageFilter, ImageEnhance
import math, random, base64
from cStringIO import StringIO

cs = '0123456789'
pp = {'0':[ ['L',(0.2,0),(0.8,0),(0.8,1),(0.2,1)], ['L',(0.3,0.1),(0.7,0.1),(0.7,0.9),(0.3,0.9)] ],
      '1':[ ['L',(0.3,0),(0.55,0),(0.55,0.9),(0.8,0.9),(0.8,1),(0.2,1),(0.2,0.9),(0.45,0.9),(0.45,0.1),(0.3,0.1)] ],
      '2':[ ['L',(0.2,0),(0.8,0),(0.8,0.55),(0.3,0.55),(0.3,0.9),(0.8,0.9),(0.8,1),(0.2,1),(0.2,0.45),(0.7,0.45),(0.7,0.1),(0.2,0.1)] ],
      '3':[ ['L',(0.2,0),(0.8,0),(0.8,1),(0.2,1),(0.2,0.9),(0.7,0.9),(0.7,0.55),(0.2,0.55),(0.2,0.45),(0.7,0.45),(0.7,0.1),(0.2,0.1)] ],
      '4':[ ['L',(0.2,0),(0.3,0),(0.3,0.45),(0.7,0.45),(0.7,0),(0.8,0),(0.8,1),(0.7,1),(0.7,0.55),(0.2,0.55)] ],
      '5':[ ['L',(0.2,0),(0.8,0),(0.8,0.1),(0.3,0.1),(0.3,0.45),(0.8,0.45),(0.8,1),(0.2,1),(0.2,0.9),(0.7,0.9),(0.7,0.55),(0.2,0.55)] ],
      '6':[ ['L',(0.2,0),(0.8,0),(0.8,0.1),(0.3,0.1),(0.3,0.45),(0.8,0.45),(0.8,1),(0.2,1)], ['L',(0.3,0.55),(0.7,0.55),(0.7,0.9),(0.3,0.9)] ],
      '7':[ ['L',(0.2,0),(0.8,0),(0.8,1),(0.7,1),(0.7,0.1),(0.2,0.1)] ],
      '8':[ ['L',(0.2,0),(0.8,0),(0.8,1),(0.2,1)],['L',(0.3,0.1),(0.7,0.1),(0.7,0.45),(0.3,0.45)],['L',(0.3,0.55),(0.7,0.55),(0.7,0.9),(0.3,0.9)] ],
      '9':[ ['L',(0.2,0),(0.8,0),(0.8,1),(0.2,1),(0.2,0.9),(0.7,0.9),(0.7,0.55),(0.2,0.55)],['L',(0.3,0.1),(0.7,0.1),(0.7,0.45),(0.3,0.45)] ],
     }
def draw_char(img,char,x,y,px,linecolor):
    #双线画字体（空心字）
    draw = ImageDraw.Draw(img)
    # draw.rectangle((x,y,x+px,y+px), outline=linecolor, fill=(255,255,255)) #画外框线
    #画10x10网格线
    # for j in range(y,y+px+px/10,px/10):
    #     draw.line((x,j,x+px,j),fill=(192,192,192))
    # for i in range(x,x+px+px/10,px/10):
    #     draw.line((i,y,i,y+px),fill=(192,192,192))
    for pos in pp.get(char,[]):
        if len(pos)==0:
            continue
        tt = pos[0]       #线条类型
        points = pos[1:]  #线条坐标
        if tt=='L':
            for j in xrange(0,len(points)):
                if j<len(points)-1:
                    draw.line((x+px*points[j][0],y+px*points[j][1],x+px*points[j+1][0],y+px*points[j+1][1]),fill=linecolor)
                else:
                    draw.line((x+px*points[j][0],y+px*points[j][1],x+px*points[0][0],y+px*points[0][1]),fill=linecolor)
        elif tt=='l':
            for j in xrange(0,len(points)):
                if j<len(points)-1:
                    draw.line((x+px*points[j][0],y+px*points[j][1],x+px*points[j+1][0],y+px*points[j+1][1]),fill=linecolor)
        elif tt=='C':
            rect = (int(x+px*points[0][0]),int(y+px*points[0][1]),int(x+px*points[0][2]),int(y+px*points[0][3]))
            draw.arc(rect,points[1],points[2],fill=linecolor)
    del draw
    return img
def contortImage(img):
    """扭曲图像"""
    #params中值的含义见http://effbot.org/imagingbook/image.htm
    params = [1 - float(random.randint(1, 2)) / 50, 0, 0,
              0, 1 - float(random.randint(1, 2)) / 200, float(random.randint(1, 2)) / 500,
              0.001, float(random.randint(1, 2)) / 500]
    img = img.transform(img.size, Image.PERSPECTIVE, params, fill=1)
    #img = img.rotate(random.randint(-15,15))
    return img

def drawNoise(img,rect,linecolor,number=30):
    """在图像上画噪声，随机取字库中线条作为噪声线条，rect为指定在img的某个区域画噪声"""
    width = img.size[0]  #宽度
    height = img.size[1]  #高度
    draw = ImageDraw.Draw(img)
    for i in xrange(0,number):
        px = rect[2] #random.randint(height*0.8,height*2)  #字符大小不能太小，噪声线条才会足够大
        x = rect[0] #random.randint(0,width-px)
        y = random.randint(0,height/2)
        index = random.randint(0,len(cs)-1)
        cc1 = pp.get(cs[index],[])              #随机取字库的一个字符
        cc2 = cc1[random.randint(0,len(cc1)-1)] #随机取字符的一组线条
        tt = cc2[0]       #线条类型
        points = cc2[1:]  #线条坐标
        if tt=='L' or tt=='l':
            j = random.randint(0,len(points)-1) #随机取一个线条
            if j<len(points)-1:
                draw.line((x+px*points[j][0],y+px*points[j][1],x+px*points[j+1][0],y+px*points[j+1][1]),fill=linecolor)
            else:
                draw.line((x+px*points[j][0],y+px*points[j][1],x+px*points[0][0],y+px*points[0][1]),fill=linecolor)
        elif tt=='C':
            rect = (int(x+px*points[0][0]),int(y+px*points[0][1]),int(x+px*points[0][2]),int(y+px*points[0][3]))
            draw.arc(rect,points[1],points[2],fill=linecolor)
    del draw
def createVerifyCodeImage(charnumber=4,imgH=30):
    """生成验证码图像，输入字符个数"""
    retval = ''
    for i in xrange(0,charnumber):
        index = random.randint(0,len(cs)-1)
        retval = retval + cs[index]
    return retval,drawVerifyCodeImage(retval)
def drawVerifyCodeImage(text,imgH=30):
    """生成验证码图像，输入验证码字符"""
    height = imgH  #高度
    width = height*len(text)  #宽度
    linecolor = (128,128,128) #线的颜色
    border = height/10  #为了扭曲字符后不缺少笔划轮廓，字符大小扩展
    imout = Image.new(mode='RGBA',size=(width,height),color=(255,255,255,0)) #A通道为0使背景透明
    lastx = 0 #random.randint(0,width/10) #第1个字符x坐标
    lastpx = random.randint(5,height-10-border) #上一个字符大小
    i = 1
    # imout.save('o%d.png'%i)
    i += 1
    drawNoise(imout,(lastx,0,lastx+lastpx,height),linecolor,5) #在左侧空白处添加噪声
    # imout.save('o%d.png'%i)
    i += 1
    for char in text:
        px = random.randint(height/2,height-10-border) #当前字符大小
        xadd = random.randint(int(lastpx*0.8),int(lastpx*1.8)) #当前字符输出位置x坐标(在上一个字符x坐标的基础上向右移动0.8-1.8倍上一字符宽度)
        drawNoise(imout,(lastx+lastpx,0,lastx+lastpx+xadd,height),linecolor,10) #在左侧空白处添加噪声
        # imout.save('o%d.png'%i)
        i += 1
        x = lastx + xadd
        if x+px>width:
            x = width-px-border
        y = random.randint(0,height-px)                         #当前字符输出位置y坐标
        img = Image.new(mode='RGBA',size=(px,px),color=(255,255,255,0)) #A通道为0使背景透明
        draw_char(img,char,border/2,border/2,px-border,linecolor) #画字符
        #img.save('%s.png'%char,'PNG') #保存单个字符图像
        img = contortImage(img)
        imout.paste(img,(x,y))
        # imout.save('o%d.png'%i)
        i += 1
        lastpx = px
        lastx = x
    drawNoise(imout,(lastx+lastpx,0,lastx+lastpx+xadd,height),linecolor,10) #在图像右侧空白处添加噪声
    # imout.save('o%d.png'%i)
    i += 1
    drawNoise(imout,(0,0,imout.size[0],imout.size[1]),linecolor,15) #整个图像范围内的随机噪声
    # imout.save('o%d.png'%i)
    i += 1
    return imout
def getImageBase64(img):
    """输出一个PIL Image对象，返回该对象保存为png格式的文件的base64编码"""
    o = StringIO()
    img.save(o, "PNG")
    return base64.b64encode(o.getvalue())

def showFonts():
    """生成字体样例图片"""
    px = 300 #字体大小
    x = px/10 #起始
    y = px/10 #起始
    space = px/10 #间隔
    linecolor = (0,0,0) #线的颜色
    width = 8*(px+space)+2*x
    height = 5*(px+space)+2*y
    imout = Image.new(mode='RGBA',size=(width,height),color=(255,255,255,0)) #A通道为0使背景透明
    for c in cs:
        draw_char(imout,c,x,y,px,linecolor)
        if x+px+px<width:
            x = x+px+space
        else:
            x = px/10
            y = y+px+space
    imout.save('fonts.png','PNG')

if __name__ == '__main__':
    # 字体图集
    # showFonts()

    # 随机字符的验证码
    code,img = createVerifyCodeImage(4)
    print getImageBase64(img)

    # 给定字符的验证码
    # img = drawVerifyCodeImage('DONG')

    # 输出和显示
    #img.save('imout.png','PNG')
    #img.show()

    # 生成几十个验证码来查看生成效果
    # for i in xrange(1,30):
    #     code, img = createVerifyCodeImage(4)
    #     img.save('imout%d.png'%i,'PNG')
