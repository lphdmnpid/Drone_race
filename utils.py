import cv2, sys
from ultralytics import YOLO
import numpy as np

RACE_INFO = None
RACE_RESULTS = None
RACE_COUNT = 4
MIN_CURRENCY = 0.8
FRAMES_COUNT = 2
FRAMES_DELAY = 3
TOTAL_SIZE = 0.4
SIZE_RANGE = 0.1
try:
	MODEL = YOLO(sys.argv[1])
except:
	MODEL = YOLO("last.pt")

def process_frame(frm, ind = 0):
	global RACE_INFO, RACE_RESULTS

	if RACE_INFO is None:
		RACE_INFO = [[0,-1,0,0] for i in range(RACE_COUNT)] # class, frames_before, size_before, frames_count
	if RACE_RESULTS is None:
		RACE_RESULTS = [0 for i in range(RACE_COUNT)]

	result = MODEL.predict(frm, verbose = False)
	boxes = result[0].boxes.xyxy.cpu().numpy()
	confidences = result[0].boxes.conf.cpu().numpy()
	classes = result[0].boxes.cls.cpu().numpy()

	if (RACE_INFO[ind][1] >= 0):
		RACE_INFO[ind][1] -= 1

	cur_clss = 0
	cur_size = 0
	h, w = frm.shape[0], frm.shape[1]
	for box, conf, clss in zip(boxes, confidences, classes):
		x1, y1, x2, y2 = map(int, box)
		cv2.rectangle(frm, (x1, y1), (x2, y2), (0, 255, 0), 2)
		cv2.putText(frm, f"{int(clss)}: {conf:.2f}", (x1 + 5, y1 + 15),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		if conf >= MIN_CURRENCY:
			size = (x2-x1)/w*(y2-y1)/h
			if (cur_size < size):
				cur_clss = clss
				cur_size = size
	
	if (RACE_INFO[ind][1] == 0 and RACE_INFO[ind][2] >= TOTAL_SIZE and RACE_INFO[ind][3] >= FRAMES_COUNT):
		if RACE_INFO[ind][0] == 0:
			RACE_RESULTS[ind] += 1
		else:
			RACE_RESULTS[ind] = 0
	
	if (cur_size != 0 and (cur_size + SIZE_RANGE >= RACE_INFO[ind][2] or RACE_INFO[ind][1] == -1)):
		if (RACE_INFO[ind][1] == -1 or RACE_INFO[ind][0] != cur_clss):
			RACE_INFO[ind][0] = cur_clss
			RACE_INFO[ind][1] = FRAMES_DELAY
			RACE_INFO[ind][2] = cur_size
			RACE_INFO[ind][3] = 1
		else:
			RACE_INFO[ind][1] = FRAMES_DELAY
			RACE_INFO[ind][2] = cur_size
			RACE_INFO[ind][3] += 1

	cv2.putText(frm, f"{RACE_RESULTS[ind]}", (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 139), 2)

	return frm

def show_frame(main_frame):
	"""
	right - 83
	left - 81
	up - 82
	down - 84

	plus - 43
	minus - 45

	w - 119
	e - 101
	s - 115
	d - 100
	r - 114
	f - 102

	enter - 13
	esc - 27
	space - 32

	1-9 / 49-57
	"""
	while (1):
		cv2.imshow("", main_frame)
		key = cv2.waitKey(0)
		match key:
			case 32:	#enter
				return True, 0
			case 13:	#enter
				return True, 0
			case 27:	#esc
				return True, 1
			case 113:	#q
				return False, 0
			case -1:
				return False, 0

def convert_frame(frame):
	new_frame = (frame * np.array([0, 1, 1])).astype(np.uint8)
	return new_frame
