#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
import scratch
import socket
import time
import sys
import rospy
import roslib
import re
from std_msgs.msg import Int16
from std_msgs.msg import String
from std_msgs.msg import Bool
from pcl_test.msg import stringArray
from subprocess import Popen



def voiceCallback(msg):#order
	if 'korean' in msg or 'soup' in msg or 'Korean' in msg:
		s.broadcast('order_korean_soup')
	elif 'noodle' in msg or 'Noodle' in msg:
		s.broadcast('order_cup_noodle')
	elif 'chip' in msg or 'Chip' in msg or 'Star' in msg:
		s.broadcast('order_chip_star')

def object_cb(msg):#検出されたオブジェクト名を送信
	for i in range(0,len(msg.data)):
		s.broadcast(msg.data[i])

def arrive_cb(msg):#到着判定
	s.broadcast(msg.data)
	rospy.loginfo(msg.data)

def grasp_Callback(msg):
	rospy.loginfo("Grasp ok")
	s.broadcast('get_object')

if __name__ == '__main__':
	rospy.init_node('scratch_connector')
	rospy.loginfo("scratch_connector started")
	
	s = scratch.Scratch()

	sub_recog_word = rospy.Subscriber("/recognition_word", String, voiceCallback)#音声認識
	sub_detect_object_name = rospy.Subscriber("/detect_object_name_array", stringArray,object_cb)#物体認識
	sub_arrival = rospy.Subscriber("/arrive_msg", String, arrive_cb)#自立移動
	sub_grasp_flag = rospy.Subscriber("/grasp_flag", Bool, grasp_Callback)#マニプレーション

	pub_speech_word = rospy.Publisher('/speech_word', String)#音声合成
	pub_move_ctrl = rospy.Publisher('/move_ctrl',String)#自立移動
	pub_od_ctrl = rospy.Publisher('/object_detection_contrl',Bool)#物体認識の開始,停止
	pub_grasp_obj_by_frame = rospy.Publisher('/grasp_obj_by_frame',String)#マニプレーション
	pub_put_ctrl = rospy.Publisher('/put_object',String)#物体配置

	get_msg = ''

	while not rospy.is_shutdown():
		
		msg = s.receive()
		if msg[0] == 'broadcast':
			get_msg = msg[1]
			rospy.loginfo(get_msg)

		if(get_msg.find('say') >= 0):
			word = get_msg[4:len(get_msg)]
			rospy.loginfo(word)
			pub_speech_word.publish(word)

		elif(get_msg.find('move') >= 0):
			word = get_msg[5:len(get_msg)]
			rospy.loginfo(word)
			pub_move_ctrl.publish(word)

		elif(get_msg.find('grasp') >= 0):
			word = get_msg[6:len(get_msg)]
			rospy.loginfo(word)
			pub_grasp_obj_by_frame.publish(word)

		elif(get_msg.find('put') >= 0):
			word = get_msg[4:len(get_msg)]
			rospy.loginfo(word)
			pub_put_ctrl.publish(word)

		elif(get_msg.find('object_detection_start') >= 0):
			pub_od_ctrl.publish(True)

		elif(get_msg.find('object_detection_stop') >= 0):
			pub_od_ctrl.publish(False)


