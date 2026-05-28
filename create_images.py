import cv2
import numpy as np
import os


coords = [[0,0], [120,120]]
step = 10
def process_frame(main_frame):
	global step
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
	all_coords = [[] for i in range(9)]
	frame = main_frame.copy()
	h,w = main_frame.shape[0], main_frame.shape[1]
	while (1):
		cur_frame = cv2.rectangle(frame.copy(), coords[0], coords[1], (0,255,255))
		cv2.putText(cur_frame, str(step), [5, 15], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
		cv2.imshow("", cur_frame)
		key = cv2.waitKey(0)
		match key:
			case 82: #up
				coords[0][1] -= step
				coords[1][1] -= step
			case 84: #down
				coords[0][1] += step
				coords[1][1] += step
			case 81: #left
				coords[0][0] -= step
				coords[1][0] -= step
			case 83: #right
				coords[0][0] += step
				coords[1][0] += step
			
			case 43: #plus
				step += 1
			case 45: #minus
				step -= 1

			case 119: #w
				coords[1][0] -= step
			case 101: #e
				coords[1][0] += step
			case 115: #s
				coords[1][1] -= step
			case 100: #d
				coords[1][1] += step

		
			case 13:	#enter
				return True, all_coords
			case 27:	#esc
				return True, 1
			case 32: #space
				return True, []
			case 113:	#q
				return False, []
			case -1:
				return False, []
			case _:
				if (key > 48 and key < 58):
					if (all_coords[key-49] == coords):
						all_coords[key-49] = []
					else:
						all_coords[key-49] = []
						all_coords[key-49].append(coords[0].copy())
						all_coords[key-49].append(coords[1].copy())
						i = key-49
						for j in range(2):
							all_coords[i][j][0] = max(0, all_coords[i][j][0])
							all_coords[i][j][0] = min(w, all_coords[i][j][0])
							all_coords[i][j][1] = max(0, all_coords[i][j][1])
							all_coords[i][j][1] = min(h, all_coords[i][j][1])
					frame = main_frame.copy()
					for j in all_coords:
						if j != []:
							frame = cv2.rectangle(frame, j[0], j[1], (0,255,0))


cap = cv2.VideoCapture("vid.mp4")


flag = True
rev_flag = False

ind = 0
num = 0
try:
	with open("info.txt") as f:
		ind = int(f.readline())
		num = int(f.readline())
		rev_flag = True
except:
	pass

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

	frm = frame_images[1]

	flag, info = process_frame(frm)
	if info == 1:
		rev_flag = True
	elif info != []:
		cv2.imwrite(f"./images/frame{num}.png", frm)
		with open(f"./objects/frame{num}.txt", "w") as f:
			for i in info:
				if i != []:
					x_0, y_0, w, h = min(i[0][0], x_line)/x_line, min(i[0][1], y_line)/y_line, (min(i[1][0], x_line) - min(i[0][0], x_line))/x_line, (min(i[1][1], y_line) - min(i[0][1], y_line))/y_line
					f.write(f"0 {x_0 + w/2} {y_0 + h/2} {w} {h}\n")
		num += 1


with open("info.txt", "w") as f:
	f.write(str(ind) + "\n")
	f.write(str(num))

cap.release()
cv2.destroyAllWindows()
