# -*- coding: utf-8 -*-

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import time
import datetime
import sys
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("C:\\Project\\MonkeyRunner\\refactor\\config.ini")

ENV = sys.argv[1]
ACTION = sys.argv[2]
TIMES = sys.argv[3]
DEVICE = Config.get(ENV, 'device')
VICTORY_LOOP = 30


class CommonAction:
	def __init__(self, steps, device):
		self.steps = steps
		self.device = device
		self.defautl_loop = 10

	def action_step(self, step):
		location_y = step[0]
		location_x = step[1]
		wait = step[2]
		action = step[3]
		print "going to " + action
		time.sleep(wait)
		if action_step == 'victory':
			wait_loop = VICTORY_LOOP
		else:
			wait_loop = self.defautl_loop
		if len(step) == 5:
			sub_img_location = step[4]
			for i in range(wait_loop):
				if compare_image(sub_img_location, action):
						break
					time.sleep(2)
		now_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
		if action == 'result':
			result.writeToFile('D:\\yinyang\\win_result\\test_%s_%s.png'%(now_string, action),'png')
		self.device.touch(location_y, location_x,'DOWN_AND_UP')
		
		
	def compare_image(self, sub_img_location, action):
		result = self.device.takeSnapshot()
		sub_img = result.getSubImage(sub_img_location)
		target = MonkeyRunner.loadImageFromFile('D:\\yinyang\\win\\test_%s.png'%(action))
		if sub_img.sameAs(target, 0.8):
			return True

	def execute_script(self):
		for step in self.steps:
			print datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
			self.action_step(step)

yuhun_steps = [
	#[952, 524, 5, 'start', (130, 1110, 70, 100)],
	# [952, 524, 10, 'start'],
	# # [1162, 554, 2, 'again'],
	# [1162, 554, 80, 'fight',(490, 420, 90, 120) ],
	# #[608, 554, 1, 'gift', (270, 580, 80, 100) ],
	# [608, 554, 2, 'gift'],
	# [594, 416, 3, 'result', (130, 580, 80, 100)],
	# [760, 608, 2, 'done',(155, 890, 55, 125)]
	# [680, 430, 10, 'start'],
	[720, 490, 5, 'team',(670, 460, 125, 40)],
	[880, 440, 5, 'fight',(820, 540, 115, 50)],
	[475, 575, 30, 'victory',(315, 110, 100, 75)],
	[475, 575, 3, 'gift'],
	[475, 575, 5, 'result', (425, 425, 100, 60)],
	[550, 370, 5, 'invite',(310, 220, 330, 160)]
]

master_steps = ['team', 'fight', 'victory', 'gift', 'result', 'invite']
parner_steps = ['invited','fight', 'victory', 'gift', 'result']
self_steps = ['start','fight', 'victory', 'gift', 'result']

def read_step(step):
	value = Config.get(ENV, step)
	step_array = value.split(', ')
	if len(step_array) >= 5:
		step_array[4] = tuple(map(int, step_array[4].split('-')))
	for i in range(3):
		step_array[i] = int(step_array[i])
	return step_array

def get_action_steps(ACTION):
	final_steps = []
	if ACTION == 'master':
		action_steps = master_steps
	elif ACTION == 'parner':
		action_steps = parner_steps
	else:
		action_steps = self_steps

	for step in action_steps:
		final_steps.append(read_step(step))
	return final_steps

# device = MonkeyRunner.waitForConnection(30, DEVICE)


# Aciton = CommonAction(yuhun_steps, device)
# for i in range(20):
# 	print i + 1
# 	Aciton.execute_script()

# JueXing = CommonAction(juexing_steps)
# JueXing.execute_script()

# tianzhan(device)

print get_action_steps(ACTION)