from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import time
import datetime

class CommonAction:
	def __init__(self, steps, device):
		self.steps = steps
		self.device = device

	def click_action(self, step):
		location_y = step[0]
		location_x = step[1]
		wait = step[2]
		action = step[3]
		print "going to " + action
		img_enable = False
		wait_loop = 25
		if action == 'victory':
			wait_loop = 40
		if action == 'fight':
			wait_loop = 50
		time.sleep(wait)
		if len(step) == 5:
			sub_img_location = step[4]
			for i in range(wait_loop):
				result = self.device.takeSnapshot()
				sub_img = result.getSubImage(sub_img_location)
				target = MonkeyRunner.loadImageFromFile('./mobile/test_%s.png'%(action))
				print i
				if sub_img.sameAs(target, 0.8):
					img_enable = True
					break
				if action == 'invited':
					time.sleep(0.5)
				else:
					time.sleep(1)
			if img_enable:
				print "get the screenshot"
			else:
				print "not able to get the screenshot"
		now_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
		if action == 'result':
			result = self.device.takeSnapshot()

		self.device.touch(location_y, location_x,'DOWN_AND_UP')
		

	def execute_script(self):
		for step in self.steps:
			print datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
			self.click_action(step)

yuhun_steps = [
	# [65, 240, 5, 'invited',(40, 215, 50, 50)],
	# [205, 390, 0.5, 'yes'],
	# # [952, 524, 5, 'start', (150, 890, 60, 130)],
	[1750, 830, 5, 'fight', (1630, 985, 240, 70)],
	[950, 1040, 10, 'victory', (600, 200, 250, 180)],
	[608, 554, 3, 'gift'],
	[950, 1040, 5, 'result',(800, 750, 300, 150)],
	# [65, 240, 5, 'invited', (40, 215, 50, 50)]
	#win
	# [720, 410, 5, 'start',(670, 410, 100, 45)],
	# [880, 440, 5, 'fight',(820, 540, 115, 50)],
	# [475, 575, 100, 'victory',(315, 110, 100, 75)],
	# [475, 575, 3, 'gift'],
	# [475, 575, 5, 'result', (425, 425, 100, 60)],
]




device = MonkeyRunner.waitForConnection(30,'3636dcdb')


Aciton = CommonAction(yuhun_steps, device)
for i in range(20):
	print i + 1
	Aciton.execute_script()
