import numpy as np
import cv2

from os import listdir
from os.path import isfile, join

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


files = GetListOfOutputFilesNumeric("C:/Users/Moon/Desktop/Summer Research/TACOS/pics/Subtracted/s27-d45/", "sub", 1, 4910, "jpg")
print files

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))

count = 0

for filePath in files:
  count = count + 1
  print count
  image = cv2.imread(filePath)
  morphedIMG = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

  outfile = "C:/Users/Moon/Desktop/Summer Research/TACOS/pics/Morphological/s30-d40/morph%d.jpg" % count

  cv2.imwrite(outfile, morphedIMG)

cv2.destroyAllWindows()
