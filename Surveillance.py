from PIL import Image
import time,picamera,os,sys,io
from sense_hat import SenseHat

def newImage():
    global stream
    stream.seek(0)
    camera.capture(stream,format='jpeg')
    stream.seek(0)
    return list(Image.open(stream).getdata())

with open("/home/pi/Documents/SurveillanceRunning.txt",'w') as file:
    file.write(str(os.getpid()))
stream=io.BytesIO()    
camera=picamera.PiCamera()
camera.vflip=camera.hflip=True
sense=SenseHat()
sense.load_image("/home/pi/Documents/interrogation.png")
redColor=[[255,0,0] for i in range(0,64)]
r=[255,0,0]
b=[255,255,255]
exclamation=[r,r,r,b,b,r,r,r,
             r,r,r,b,b,r,r,r,
             r,r,r,b,b,r,r,r,
             r,r,r,b,b,r,r,r,
             r,r,r,b,b,r,r,r,
             r,r,r,r,r,r,r,r,
             r,r,r,b,b,r,r,r,
             r,r,r,b,b,r,r,r]
newPhoto=newImage()
while True:
    oldPhoto=newPhoto
    newPhoto=newImage()
    differents=0
    for i in range(0,len(oldPhoto),500):
        if newPhoto[i][0]-50>oldPhoto[i][0]  or newPhoto[i][0]+50<oldPhoto[i][0] or newPhoto[i][1]-50>oldPhoto[i][1] or newPhoto[i][1]+50<oldPhoto[i][1] or newPhoto[i][2]-50>oldPhoto[i][2]  or newPhoto[i][2]+50<oldPhoto[i][2] :
            differents+=1
    if differents/(len(oldPhoto)/500)>0.02:
        nom=time.strftime("%Y")+"-"+time.strftime("%m")+"-"+time.strftime("%d")+"_"+time.strftime("%X")
        Image.open(stream).save("/home/pi/Documents/PhotosSurveillance/"+nom+".jpg")
        camera.start_recording("/home/pi/Documents/video.h264")
        for k in range(10):
            sense.set_pixels(redColor)
            time.sleep(1)
            sense.set_pixels(exclamation)
            time.sleep(1)
        camera.stop_recording()
        os.system("sudo MP4Box -add /home/pi/Documents/video.h264 /home/pi/Documents/VideosSurveillance/"+nom+".mp4")
        os.unlink('/home/pi/Documents/video.h264')
        newPhoto=newImage()
        sense.load_image("/home/pi/Documents/interrogation.png")
