# !usr/bin/python3
# encoding: utf-8
# author: Huang Jingxiong

import numpy as np
import cv2 as cv
import os

# ROI参数，通过矩形左上角坐标和宽高确定一个矩形区域
roi_x = 70
roi_y = 51
roi_w = 107
roi_h = 87


def empty_hist():
	hist = []
	for i in range(0, 16):
		hist.append(0)
	return hist


def gray():
	bin = []
	count = 0
	for i in range(0, 16):
		while count < 16:
			bin.append(i)
			count += 1
		count = 0
	return bin


def gray_hist(img):
	height, width = img.shape[0], img.shape[1]
	cx = width / 2
	cy = height / 2
	weight_c = []
	# 带宽
	band = pow(cx, 2) + pow(cy, 2)

	# 初始化灰度和直方图
	bin = gray()
	hist = empty_hist()

	for i in range(0, height):
		for j in range(0, width):
			color = img[i][j]
			color_bin = bin[color]
			distance = pow(i - cy, 2) + pow(j - cx, 2)
			weight = 1 - distance / band
			weight_c.append(weight)
			hist[color_bin] += weight
	# 计算目标权值直方
	C = sum(weight_c)
	# 归一化系数
	if C == 0:
		C = 1
	hist = [c_bin / C for c_bin in hist]
	return hist


def get_similarity(hist1, hist2):
	similarity = []
	# 计算两个直方图的相关度
	for i in range(0, 16):
		if hist2[i] != 0:
			temp = hist1[i] / hist2[i]
			similar = np.sqrt(temp)
			similarity.append(similar)
		else:
			similarity.append(0)
	return similarity


def mean_shift(roi, roi_window, hist1, img):
	# 计算hist2，计算相似度，然后计算新的中心点，进行均值漂移
	cx, cy, w, h = roi_window
	num = 0

	# 迭代次数设置为50
	while num < 50:
		x_shift = 0
		y_shift = 0
		sum_weight = 0

		hist2 = gray_hist(roi)
		bin = gray()
		similarity = get_similarity(hist1, hist2)

		num += 1
		for i in range(0, h):
			for j in range(0, w):
				color = roi[i][j]
				# 获取每个像素点内颜色的bin
				color_bin = bin[color]
				sum_weight += similarity[color_bin]
				# 迭代计算漂移向量
				y_shift += similarity[color_bin] * (i - h / 2)
				x_shift += similarity[color_bin] * (j - w / 2)
		# 计算权重总和
		if sum_weight == 0:
			sum_weight = 1
		y_shift /= sum_weight
		x_shift /= sum_weight
		cx += x_shift * 1.69
		cy += y_shift * 1.69
		cx = np.around(cx).astype(int)
		cy = np.around(cy).astype(int)
		roi = img[cy: cy + h, cx: cx + w]
	return cx, cy


def main(video):
	cap = cv.VideoCapture(video)
	count = 0
	total_number = cap.get(cv.CAP_PROP_FRAME_COUNT)

	while count < total_number:
		ret, img = cap.read(10)
		x, y, w, h = roi_x, roi_y, roi_w, roi_h

		# 定位所要跟踪的物体
		roi = img[y: y + h, x: x + w]
		roi = cv.cvtColor(roi, cv.COLOR_RGB2GRAY)
		roi_hist = gray_hist(roi)

		# 为每帧计算均值漂移
		img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
		roi_next = img[y:y + h, x:x + w]
		tx, ty = mean_shift(roi_next, (x, y, w, h), roi_hist, img)
		# 均值漂移的新位置
		img = cv.rectangle(img, (tx, ty), (tx + w, ty + h), 255, 2)
		cv.imwrite(r'.\Output\\' + '%04d' % count + '.jpg', img)
		print('Now processing: ' + '%04d' % count + '.jpg')
		count += 1
	cap.release()


if __name__ == "__main__":
	if os.path.exists('.\Output') is False:
		os.mkdir('.\Output')
	video = 'Video.avi'
	main(video)
