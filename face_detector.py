import cv2
import numpy

from os import listdir
from os.path import isfile, join




#############################################
def GetListOfFiles(dir_path, file_type):

  files = [f for f in listdir(dir_path) if isfile(join(dir_path,f))]
  out_files = []
  filetype_len = len(file_type)
  for filename in files:
    if len(filename) < filetype_len:
      continue
    if filename[-1 * filetype_len:] == file_type:
      out_files.append(join(dir_path,filename))
  return out_files
############################################



###########################
def ExtractFaces(video_file_path):
  """Play a short video clip from the given video file."""
  video = cv2.VideoCapture(video_file_path)
  print video
  nFrames = (int)(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
  print nFrames
  framerate = video.get(cv2.cv.CV_CAP_PROP_FPS)

  vidStart = 0
  vidLength = nFrames
  
  # start_frame = int(start_time * float(framerate))
  # end_frame = int(end_time * float(framerate))
  
  # if end_frame > nFrames:
  #   end_frame = nFrames - 1
  # print start_frame, end_frame

  face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

  frame_list = []
  total_facecount = 0
  for i in range(vidStart, vidLength):
    print video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    #ret, frame = video.read()
    if video.grab():
      ret, frame = video.retrieve()
    # cv2.waitKey(1000)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #cl1 = clahe.apply(gray)

    faces = face_cascade.detectMultiScale(equ, 1.3, 5)
    if len(faces) > 0:
      total_facecount += 1
    print len(faces)
    print total_facecount
    # face_count = 0
    # for (x,y,w,h) in faces:
    #   area = w*h
    #   print area
    #   if area < 4000.0:
    #     continue
    
    #   cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    #   roi_gray = gray[y:y+h, x:x+w]
    #   resized_image = cv2.resize(roi_gray, (200, 200))
    #   image_filename = "./faces/%d_%d.jpg" % (i, face_count)
    #   face_count = face_count + 1
    #   # cv2.imwrite(image_filename,resized_image)
    #   # roi_color = img[y:y+h, x:x+w]
    #   # resize the roi_gray and write to a file
      
    # cv2.imshow(video_file_path, frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #  break

  video.release()
  # cv2.destroyAllWindows()
  return total_facecount, nFrames

###########################

path = "./test/"
files = GetListOfFiles(path, ".avi")
f = open('face_numbers.txt','a')
for i in range(len(files)):
  num, numFrames = ExtractFaces(files[i])
  f.write("%s,%d,%d\n" % (files[i], numFrames, num))

