import cv2
import numpy

path = 'C:/Users/Moon/Desktop/Summer Research/TACOS/pics/Test/s30-d40.avi'

video = cv2.VideoCapture(path)
frameRate = video.get(cv2.cv.CV_CAP_PROP_FPS)
nFrames = (int)(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
print nFrames
print frameRate

count = 1
while(True):
  #print count
  #video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, count)
  print video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
  #ret, frame = video.read()
  if video.grab():
    ret, frame = video.retrieve()
  cv2.waitKey(1000)
  if ret == False:
    print "Failed to Read"
    continue
  if count>=nFrames:
    break
  cv2.imwrite("C:/Users/Moon/Desktop/Summer Research/TACOS/pics/frames/pic%d.jpg"%count, frame)
  if count%1000 == 0:
    print count
  count = count + 1

video.release()
print count
cv2.destroyAllWindows()