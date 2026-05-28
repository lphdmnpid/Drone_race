from ultralytics import YOLO
import cv2, sys
from utils import process_frame, convert_frame

try:
	main_vid = sys.argv[2]
except:
	main_vid = "vid.mp4"

try:
	to_vid = sys.argv[3]
except:
	to_vid = "vid_other.mp4"


cap = cv2.VideoCapture(main_vid)

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(to_vid, fourcc, fps, (width, height))

while True:
	ret, frame = cap.read()
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

	for i in range(4):
		frame_images[i] = process_frame(frame_images[i], i)
		#frame_images[i] = process_frame(convert_frame(frame_images[i]), i)


	frm = cv2.vconcat([cv2.hconcat([frame_images[0], frame_images[1]]), cv2.hconcat([frame_images[2], frame_images[3]])])

	out.write(frm)

cap.release()
out.release()