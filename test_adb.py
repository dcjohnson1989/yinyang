# -*- coding: utf-8 -*-
import cv2
import time
from subprocess import call
import ConfigParser
import sys

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

ENV = sys.argv[1]
DEVICE = Config.get(ENV, 'device')
TAP_CONTINUE_LOCATION = Config.get(ENV, 'continue').split(',')
#get screen
SCREEN_SHOT = ["adb","-s",DEVICE,"shell","screencap","/sdcard/screen.png"]
GET_SCREEN = ["adb","-s",DEVICE,"pull","/sdcard/screen.png"]
#define TAP
TAP = ["adb","-s",DEVICE,"shell","input","tap"]
TAP_CONTINUE = list(TAP)
TAP_CONTINUE.extend(TAP_CONTINUE_LOCATION)

BOSS_KILL = False

COMPARE_PATH = ".\\%s\\compare\\"%(ENV)
HIGHLIGHT_PATH = ".\\%s\\highlight\\"%(ENV)

def find_image(picture_list, highlight=False):	
	call(SCREEN_SHOT)
	call(GET_SCREEN)
	#get location
	if highlight:
		picture_path_root = HIGHLIGHT_PATH
	else:
		picture_path_root = COMPARE_PATH
	#compare img
	for picture in picture_list:
		picture_path = picture_path_root + picture
		img = cv2.imread('screen.png',0)
		template = cv2.imread(picture_path,0)
		w, h = template.shape[::-1]
		res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		if max_val > 0.75 :
			print "found the image: " + picture
			return [max_loc[0] + w/2, max_loc[1] + h/2]
			if picture == "capture_boss.png":
				BOSS_KILL = True
			break
		else:
			print "it's not found: " + picture

def fight():
	time.sleep(40)
	for i in range(20):
		location = find_image(['victory.png'])
		print i
		if location:
			for i in [0, 3, 5]:
				time.sleep(i)
				call(TAP_CONTINUE)
			break
		else:
			time.sleep(5)

highlight_list = []
for i in range(6):
	highlight_list.append('capture_h%s.png'%(i+1))

for i in range(15):
	location_highlight = find_image(highlight_list, True)
	if location_highlight:
		location = location_highlight
	else:
		location = find_image(['capture_boss.png','capture.png'])
	if location:
		location_x_list = [str(location[0]), str(location[0] + 10),str(location[0] - 10)]
		location_y_list = [str(location[1]), str(location[1] + 10),str(location[1] - 10)]
		for x in location_x_list:
			for y in location_y_list:
				print "going to tap: " + x + y
				action_tap = list(TAP)
				action_tap.extend([x, y])
				call(action_tap)
		time.sleep(2)
		if find_image(['capture_boss.png','capture.png']):
			print "not able to tap"
		else:
			print "going to fight"
			fight()
			if BOSS_KILL == True:
				print "BOSS KILLED"
				time.sleep(5)
				for i in range(5):
					location = find_image(['gift.png'])
					if location:
						call(["adb","-s",DEVICE,"shell","input","tap",location[0], location[1]])
						time.sleep(2)
						call(["adb","-s",DEVICE,"shell","input","tap","800", "200"])
						time.sleep(2)
					else:
						break
				break
	else:
		search_tap = list(TAP)
		search_tap.extend(["150","450"])
		call(search_tap)
		time.sleep(5)

