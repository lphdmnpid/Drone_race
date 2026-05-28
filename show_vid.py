import cv2
import numpy as np
from utils import *

cap = cv2.VideoCapture("vid_other.mp4")


flag = True
rev_flag = True

ind = 0

while flag:
	if rev_flag:
		cap.set(cv2.CAP_PROP_POS_FRAMES, ind)
		ret, frame = cap.read()
		rev_flag = False
		ind -= 1
	else:
		ret, frame = cap.read()
		ind += 1
	if not ret:
		break
	
	x_line = frame.shape[1]//2
	y_line = frame.shape[0]//2

	frame_images = [
		frame[0:y_line, 0:x_line],
		frame[0:y_line, x_line:],
		frame[y_line:, 0:x_line],
		frame[y_line:, x_line:]
	]

	frm = cv2.vconcat([cv2.hconcat([frame_images[0], frame_images[1]]), cv2.hconcat([frame_images[2], frame_images[3]])])

	flag, info = show_frame(frm)
	if info == 1:
		rev_flag = True

cap.release()
cv2.destroyAllWindows()
