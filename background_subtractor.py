import numpy as np
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

files = GetListOfOutputFilesNumeric("C:/Users/Moon/Desktop/Summer Research/TACOS/pics/hands/", "track", 1, 4910, "jpg")
print files
fgbg = cv2.BackgroundSubtractorMOG()

count = 0

for filePath in files:
  count = count + 1
  print count
  frame = cv2.imread(filePath)
  # print ret
  fgMaskMOG = fgbg.apply(frame)
  print type(fgMaskMOG)
  #print fgMaskMOG

  outfile = "C:/Users/Moon/Desktop/Summer Research/TACOS/pics/Subtracted/s30-d40/sub%d.jpg" % count

  cv2.imwrite(outfile, fgMaskMOG)

cv2.destroyAllWindows()