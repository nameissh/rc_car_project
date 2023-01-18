import my_object_detect
import YB_Pcb_Car  #Import Yahboom car library
import cv2
import numpy as np
from flask import Flask,request,render_template,Response,stream_with_context
import RPi.GPIO as GPIO
import time
import os,time
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_utils
import json
from json import encoder
import pymysql


car = YB_Pcb_Car.YB_Pcb_Car()
ob= my_object_detect.my_object_detect
app=Flask(__name__)
db = pymysql.connect(host='192.168.0.177', user='root', password = '4321', db='mysql', charset='utf8')
cur=db.cursor()

@app.route('/video_feed')
def video_feed():
	global cap
	return Response(ob.gen(),mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/SSSecurity')
def web_cctv():
	return render_template('my_web_cctv copy.html')


	
@app.route('/sg90_control_act')
def sg90_control_act():
	if request.method=='GET':
		servo=request.args["servo"]
		
		if servo=='A':
			car.Car_Run(700,700)
		if servo=='B':
			car.Car_Back(300,300)
		if servo=='R':
			car.Car_Right(60,0)
		if servo=='L':
			car.Car_Left(0,60)
		if servo=='S':
			car.Car_Stop()
		if servo=='AA':
			car.Car_Run(300,300)
	

		

	
		
		return render_template('my_web_cctv copy.html')
		
if __name__=='__main__':
	app.run(debug=True, port=80,host='0.0.0.0')	
		
