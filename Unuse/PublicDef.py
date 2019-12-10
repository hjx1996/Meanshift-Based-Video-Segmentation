# !/usr/bin/python3
# encoding: utf-8

import numpy as np


def gray_64bin():
    bin = []
    count = 0
    for i in range(0,64):
        while count < 4:
            bin.append(i)
            count += 1
        count = 0
    return bin


def gray_32bin():
    bin = []
    count = 0
    for i in range(0,32):
        while count < 8:
            bin.append(i)
            count += 1
        count = 0
    return bin


def gray_16bin():
    bin = []
    count = 0
    for i in range(0,16):
        while count < 16:
            bin.append(i)
            count += 1
        count = 0
    return bin


def gray_bin():
    bin = []
    count = 0
    bin_num = 0
    for i in range(0,256):
        bin.append(i)
        bin_num+=1
    return bin


def RGB_empty_hist():
	hist = []
	for i in range(0, 4096):
		hist.append(0)
	return hist


def color_hist(img):
	h = img.shape[0]
	w = img.shape[1]
	hist = RGB_empty_hist()
	band = 2
	weight_c = []
	for i in range(0, h):
		for j in range(0, w):
			qr = img[i][j][0] / 16
			qg = img[i][j][1] / 16
			qb = img[i][j][2] / 16
			q_temp = qr * 239 + qg *16 + qb
			print(q_temp)
			q_temp = np.around(q_temp).astype(int)
			print(i)
			dist = pow(i - 1, 2) + pow(j - 1, 2)
			weight = 1 - dist / band
			weight_c.append(weight)
			hist[q_temp] += weight
	C = sum(weight_c)
	hist = [c_bin / C for c_bin in hist]
	return hist


def empty_hist():
	hist = []
	for i in range(0, 16):
		hist.append(0)
	return hist


def get_hist(img):
	h = img.shape[0]
	w = img.shape[1]
	bin = gray_16bin()
	hist = empty_hist()
	c_x = w / 2
	c_y = h / 2
	weight_c = []
	band = pow(c_x, 2) + pow(c_y, 2)

	for col in range(0, h):
		for row in range(0, w):
			color = img[col][row]
			color_bin = bin[color]
			dist = pow(col - c_y, 2) + pow(row - c_x, 2)
			weight = 1 - dist / band
			weight_c.append(weight)
			hist[color_bin] += weight
	C = sum(weight_c)
	if C == 0:
		C = 1
	hist = [c_bin / C for c_bin in hist]
	return hist


def get_similarity(hist1, hist2):
	similar = []
	for i in (range(0, 16)):
		if hist2[i] != 0:
			temp = hist1[i]/hist2[i]
			similarity = np.sqrt(temp)

			similar.append(similarity)
		else:
			similar.append(0)
	return similar


def meanshift_step(roi,roi_window,hist1,img):
	# 1 calculate h2
	# 2 calculate similarity
	# 3 calculate new center
	box_cx, box_cy, box_w, box_h = roi_window
	len = box_h*box_w
	num = 0
	sim = []
	sum_w = 0

	while num < 50:
		x_shift = 0
		y_shift = 0
		sum_w = 0
		hist2 = get_hist(roi)
		bin = gray_16bin()
		similarity = get_similarity(hist1, hist2)
		num += 1

		for col in range(0, box_h):
			for row in range(0, box_w):
				color = roi[col][row]
				color_bin = bin[color]
				# 计算normalize 的底
				sum_w = sum_w + similarity[color_bin]

				y_shift = y_shift + similarity[color_bin]*(col-box_h/2)
				x_shift = x_shift + similarity[color_bin]*(row-box_w/2)

		if sum_w == 0:
			sum_w = 1
		y_shift = y_shift/sum_w
		x_shift = x_shift/sum_w

		box_cx += x_shift * 1.69
		box_cy += y_shift * 1.69

		box_cx = np.around(box_cx).astype(int)
		box_cy = np.around(box_cy).astype(int)

		roi = img[box_cy:box_cy + box_h, box_cx:box_cx + box_w]

	return box_cx,box_cy
