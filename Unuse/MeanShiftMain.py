# !/usr/bin/python3
# encoding: utf-8

import PublicDef
import cv2 as cv

FONT = cv.FONT_HERSHEY_COMPLEX


def main(video_path):
    cap = cv.VideoCapture(video_path)
    count = 0
    Total_Frame_Number = cap.get(cv.CAP_PROP_FRAME_COUNT)

    roi_flag = 0
    roi_flag_t = 0
    while count < Total_Frame_Number:
        ret, img = cap.read(10)
        k = cv.waitKey(10)
        if k == ord('q'):
            break
        if k == 32:  # pause when press SPACE
            cv.waitKey(0)
        if k == ord('a'):
            # set up the ROI for tracking when press A
            roi_window = cv.selectROI('ROI', img, fromCenter=False)

            #try rgb
            x, y, w, h = roi_window
            print(roi_window)
            tx = x
            ty = y
            roi = img[y:y + h, x:x + w]
            # set rbg image to gray image
            roi = cv.cvtColor(roi, cv.COLOR_RGB2GRAY)
            roi_hist = PublicDef.get_hist(roi)
            roi_flag = 1
            cv.imshow("roi_img", roi)
            cv.waitKey(0)
            cv.destroyWindow('roi_img')
            cv.destroyWindow('ROI')

        # calculate meanshift for each frame
        if roi_flag == 1:
         # get last center
            img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            roi_next = img[y:y + h, x:x + w]
            tx, ty = PublicDef.meanshift_step(roi_next, (x, y, w, h), roi_hist, img)
            x = tx
            y = ty
            img = cv.rectangle(img, (tx, ty), (tx+w, ty+h), 255, 2)
        if roi_flag == 2:
            roi_flag = 1
        # current frame index
        count += 1
        # cv.putText(img, str(count), (40, 40), FONT, 1, (0, 0, 0), 1, cv.LINE_AA)
        cv.imshow('Video', img)

    cv.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    video_path = 'video1.avi'
    main(video_path)
