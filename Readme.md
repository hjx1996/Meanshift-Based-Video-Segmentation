#MeanShift Based Video Segmentation
Personal course work
---


* Course: Advanced in Video Analysis
* Teacher: Prof. WANG Hanzi
* Dataset: http://cvlab.hanyang.ac.kr/tracker_benchmark/datasets.html
* Final Dataset: Car4
* Challenge: IV, SV (Not final)

Including 3 python files.

## Usage
1. Running "1VideoMaker.py" to generate video from images in dataset.
2. Running "2MeanShift.py" to use meanshift model for object tracking, and the result will be output as images in /Output folder.
3. Running "3VideoMaker.py", the Video.avi in this folder will be deleted, and new Result.avi video will be generated.

## Some Question:
1. Why the video writer can't be used in one file, when I input images, I need to output video, and input video again, the model then run.
2. Meanshift model will lost its object, I should try some other method for its promotion.
