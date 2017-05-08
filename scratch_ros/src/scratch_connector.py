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

def arrive_cb(msg):
	s.broadcast(msg.data)
	rospy.loginfo(msg.data)
	if(msg.data.find('table') >= 0):
		s.broadcast('arrival_table')
	elif(msg.data.find('kitchen') >= 0):
		s.broadcast('arrival_kitchen')


def grasp_Callback(msg):
	print "grasp ok"
	s.broadcast('get_object')

if __name__ == '__main__':
	rospy.loginfo("scratch_connector started")
	rospy.init_node('scratch_connector')

	s = scratch.Scratch()

	sub_recog_word = rospy.Subscriber("/recognition_word", String, voiceCallback)
	sub_find_object_name = rospy.Subscriber("/detect_object_name_array", stringArray,object_cb)
	sub_arrival = rospy.Subscriber("/arrive_msg", String, arrive_cb)
	sub_grasp_flag = rospy.Subscriber("/grasp_flag", Bool, grasp_Callback)

	pub_speech_word = rospy.Publisher('/speech_word', String)
	pub_move_ctrl = rospy.Publisher('/move_ctrl',String)
	pub_od_ctrl = rospy.Publisher('/object_detection_contrl',Bool)
	pub_grasp_obj_by_frame = rospy.Publisher('/grasp_obj_by_frame',String)
	pub_put_ctrl = rospy.Publisher('/put_object',String)

	get_msg = ''

	while True:
		
		msg = s.receive()
		print "Scratch: receive:",msg
		if msg[0] == 'broadcast':
			get_msg = msg[1]
			print msg[1]

		if(get_msg.find('say') >= 0):
			word = get_msg[4:len(get_msg)]
			print word
			pub_speech_word.publish(word)

		elif(get_msg.find('move') >= 0):
			if(get_msg.find('table') >= 0):
				pub_move_ctrl.publish('table')
			elif(get_msg.find('kitchen') >= 0):
				pub_move_ctrl.publish('kitchen')

		elif(get_msg.find('grasp') >= 0):
			if(get_msg.find('chip') >= 0):
				pub_grasp_obj_by_frame.publish('potato_chips')
			elif(get_msg.find('noodle') >= 0):
				pub_grasp_obj_by_frame.publish('cupnoodle')
			elif(get_msg.find('soup') >= 0):
				pub_grasp_obj_by_frame.publish('korean_soup')
		
		elif(get_msg.find('put_object') >= 0):
			pub_put_ctrl.publish('put')

		elif(get_msg.find('object_detection_start') >= 0):
			Popen(['roslaunch', 'cvtest', 'obj_recog.launch'])
			rospy.sleep(3)
			Popen(['roslaunch', 'pcl_test', 'ObjectDetect.launch'])
			rospy.sleep(3)
			pub_od_ctrl.publish(True)

		elif(get_msg.find('object_detection_finish') >= 0):
			pub_od_ctrl.publish(False)

		elif(get_msg.find('object_detection_stop') >= 0):
			pub_od_ctrl.publish(False)

				
			

	


