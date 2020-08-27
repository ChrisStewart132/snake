from picamera.array import PiYUVArray
from picamera import PiCamera
import numpy as np
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 6
rawCapture = PiYUVArray(camera,size=(640,480))
width = 64*2
height = 48*2
pixelCount = width*height
#crosshair
a = np.zeros((480,640,3),dtype=np.uint8)
a[480/2,(640/2)-(width/2):(640/2)+(width/2), :]=0xff#half height or horizontal line
a[(480/2)-(height/2):(480/2)+(height/2),640/2, :]=0xff#half width or vertical line
camera.start_preview()
o = camera.add_overlay(np.getbuffer(a),layer=3,alpha=64)
prevTotal = 0.0
n = 0
for frame in camera.capture_continuous(rawCapture,format='yuv',use_video_port=True):
	image = frame.array
	rowCount = image.shape[0]#480
	columnCount = image.shape[1]#640
	colorCount = image.shape[2]#3 rgb/yuv
	#image[row][column][colors]
	total = 0.0
	max = ((rowCount/2)+(height/2),(columnCount/2)+(width/2))
	min = ((rowCount/2)-(height/2),(columnCount/2)-(width/2))	
	#print(str(max) + " " + str(min))
	for i in range(min[0],max[0]):
		for j in range(min[1],max[1]):
			total += float(image[i][j][0])
	total = total/pixelCount
	#print("total: {}".format(total))
	difference = abs(total-prevTotal)
	if n>20 and difference > 15:#checks total greyscale (Y) value for difference/movement
		print("movement detected d:{:.2f} n:{}".format(difference,n))
		name = "image{}.png".format(n)
		camera.annotate_text = "{}".format(name)
		camera.capture(name,'png')
	prevTotal = total
	n+=1
	rawCapture.truncate(0)#at end empty the capture array for next frame
camera.close()# free camera (turns it off)
