import cv2

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

###############################
def GetListOfOutputFilesNumeric(dir_path, prefix_string, min_num, max_num, file_type):
  """Read the list of files in the input directory."""
  # extract all the csv files in the directory
  out_files = []
  for i in range(min_num, max_num + 1):
    filename = "%s%d.%s"  % (prefix_string, i, file_type)
    out_files.append(join(dir_path,filename))
  return out_files


##################################



vidPath = "./s22-d48.avi"
cap = cv2.VideoCapture(vidPath)

files = GetListOfOutputFilesNumeric("./vidMorphPics", "morph", 1, 2466, "jpg")
img1 = cv2.imread("./vidMorphPics/morph1.jpg")
height, width, layers = img1.shape
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
video = cv2.VideoWriter('Moprhvideo44.avi', -1, fps, (width,height))
cap.release()

count = 1
for filePath in files:
  tempIMG = cv2.imread(filePath)
  video.write(tempIMG)
  print count
  count = count + 1

cv2.destroyAllWindows()

