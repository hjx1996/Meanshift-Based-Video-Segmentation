# !usr/bin/python3
# encoding: utf-8
# author: Huang Jingxiong

from glob import glob
import cv2 as cv
import numpy as np
import os

origin_path = r'.\Car4\img\0*.jpg'
result_path = r'.\Output\0*.jpg'

left_side = glob(origin_path)
right_side = glob(result_path)


if __name__ == "__main__":
	fourcc = cv.VideoWriter_fourcc(*'MJPG')
	video_writer_final = cv.VideoWriter('Final.avi', fourcc, 25, (720, 240))
	for i in range(len(left_side)):
		result = np.concatenate((cv.imread(left_side[i]), cv.imread(right_side[i])), axis=1)
		video_writer_final.write(result)

	if os.path.exists("Video.avi"):
		os.remove("Video.avi")
		print("执行完毕")
