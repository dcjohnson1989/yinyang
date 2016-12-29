# -*- coding: utf-8 -*-
import cv2
import time
from subprocess import call, check_output
import ConfigParser
import sys
# from PIL import Image

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

ENV = sys.argv[1]
DEVICE = Config.get(ENV, 'device')
TAP_CONTINUE_LOCATION = Config.get(ENV, 'continue').split(',')
#get screen
SCREEN_SHOT = ["adb","-s",DEVICE,"shell","screencap","/sdcard/%s.png"%(ENV)]
GET_SCREEN = ["adb","-s",DEVICE,"pull","/sdcard/%s.png"%(ENV),"%s.png"%(ENV)]
# RM_SCREEN = ["adb","-s",DEVICE,"shell","rm","-f","/sdcard/yinyang/*.png"]
# CHECK = ["adb","-s",DEVICE,"shell","ls","/sdcard/yinyang/"]
#define TAP
TAP = ["adb","-s",DEVICE,"shell","input","tap"]
TAP_CONTINUE = list(TAP)
TAP_CONTINUE.extend(TAP_CONTINUE_LOCATION)

BOSS_KILL = False

COMPARE_PATH = ".\\%s\\compare\\"%(ENV)
HIGHLIGHT_PATH = ".\\%s\\highlight\\"%(ENV)

def find_image(picture_list, highlight=False):	
	# call(RM_SCREEN)
	call(SCREEN_SHOT)
	# file_name = check_output(CHECK).strip('\r\r\n')
	# GET_SCREEN = ["adb","-s",DEVICE,"pull","/sdcard/yinyang/%s"%(file_name),"%s.png"%(ENV)]
	call(GET_SCREEN)

	# if ENV == "mobile":
	# 	img = Image.open("%s.png"%(ENV)).rotate(180)
	# 	img.save("%s.png"%(ENV))
	#get location
	if highlight:
		picture_path_root = HIGHLIGHT_PATH
	else:
		picture_path_root = COMPARE_PATH
	#compare img
	for picture in picture_list:
		picture_path = picture_path_root + picture
		img = cv2.imread("%s.png"%(ENV),0)
		template = cv2.imread(picture_path,0)
		w, h = template.shape[::-1]
		res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		if max_val > 0.75 :
			print "found the image: " + picture
			if picture == "capture_boss.png":
				print "going to kill"
				global BOSS_KILL
				BOSS_KILL = True
			return [max_loc[0] + w/2, max_loc[1] + h/2]
		else:
			print "it's not found: " + picture

def fight():
	fight_victory = False
	for j in range(10):
		time.sleep(2)
		if find_image(['fight.png']):
			call(["adb","-s",DEVICE,"shell","input","tap","870","480"])
			break
	time.sleep(20)
	for i in range(20):
		location = find_image(['victory.png'])
		print i
		if location:
			for i in [0, 3, 5]:
				time.sleep(i)
				call(TAP_CONTINUE)
			fight_victory = True
			break
		elif find_image(['fail.png']):
			call(TAP_CONTINUE)
			break
		else:
			time.sleep(5)
	return fight_victory

def action_tap(location):
	tap = list(TAP)
	tap.extend([str(location[0]), str(location[1])])
	call(tap)

challenge_count = 1

while(challenge_count < 3):
	time.sleep(2)
	location = find_image(['jiejie_2.png'])
	if location:
		action_tap(location)
		time.sleep(2)
		for i in range(5):
			challenge = find_image(['challenge.png'])
			if challenge:
				action_tap(challenge)
				if fight():
					challenge_count = challenge_count + 1
				break
			else:
				print "waiting for button display"

call(TAP_CONTINUE)
time.sleep(5)
call(TAP_CONTINUE)
time.sleep(5)

refresh_location = find_image(['refresh.png'])
if refresh_location:
	action_tap(refresh_location)
	time.sleep(2)
comfirm_location = find_image(['comfirm_refresh.png'])
if comfirm_location:
	action_tap(comfirm_location)
	time.sleep(2)