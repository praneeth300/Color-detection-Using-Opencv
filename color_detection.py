#imort the required libarries for our project
import cv2
import argparse
import pandas as pd
import numpy as np


ap=argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True,help="Image Path")
args=vars(ap.parse_args())

img_path=args["image"]

#read the image with opencv
img=cv2.imread(img_path)

clicked= False
r = g = b = xpose = ypose = False

#Next we will read the csv which contains Number of colors and their RGB codes
index=["colors","color_names","hex","R","G","B"]
df=pd.read_csv("colors.csv",names=index)

#Calculate the distance to get color name
def getcolorname(R,G,B):
    minimum=10000
    for i in range(len(df)):
        d = abs(R- int(df.loc[i,"R"])) + abs(G - int(df.loc[i,"G"])) + abs(B - int(df.loc[i,"B"]))
        if (d<=minimum):
            minimum = d
            cname= df.loc[i,"color_names"]

    return cname


def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpose,ypos, clicked
        clicked=True
        xpose=x
        ypose=y
        b,g,r=img[y,x]
        b= int(b)
        g= int(g)
        r= int(r)

#Set a mouse call back
cv2.namedWindow("image")
cv2.setMouseCallback("image",draw_function)

#Display image on the window
while (1):
    cv2.imshow("image",img)
    if (clicked):
        cv2.rectangle(img,(20,20),(750,60),(b,g,r),-1)
        text=getcolorname(r,g,b) + " R="+str(r) + " G="+str(g)+ " B="+ str(b)
        cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        if (r+g+b>=600):
            cv2.putText(img,text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        clicked=False

            #Break the loop when using press "esc"

    if cv2.waitKey(20) & 0xFF ==27:
        break

cv2.destroyAllWindows()




