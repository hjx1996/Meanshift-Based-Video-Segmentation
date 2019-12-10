# !/usr/bin/python3
# encoding: utf-8
# author: Huang Jingxiong


from glob import glob
import cv2 as cv

origin_path = r'.\Car4\img\0*.jpg'
origin = glob(origin_path)


if __name__ == '__main__':
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    video_writer = cv.VideoWriter('Video.avi', fourcc, 25, (360, 240))
    for i in range(len(origin)):
        video_writer.write(cv.imread(origin[i]))
