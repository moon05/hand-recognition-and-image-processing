##this file was previously named "detecting"

import recog
import cv2
import numpy


from os import listdir
from os.path import isfile, join

###############################
def GetListOfFiles(dir_path, file_type):
  """Read the list of files in the input directory."""
  # extract all the csv files in the directory
  files = [f for f in listdir(dir_path) if isfile(join(dir_path,f))]
  out_files = []
  filetype_len = len(file_type)
  for filename in files:
    if len(filename) < filetype_len:
      continue
    if filename[-1 * filetype_len:] == file_type:
      out_files.append(join(dir_path,filename))
  return out_files


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
def main():
  c = recog.ColorGMMSingle("./tacos-images-to-label/hand.txt")
  
  #files = GetListOfFiles("./vidPics", ".jpg")
  files = GetListOfOutputFilesNumeric("C:/Users/Moon/Desktop/Summer Research/TACOS/pics/frames", "pic", 1, 4910, "jpg")
  print files
  count = 0
  for filepath in files:
    count = count + 1
    im = cv2.imread(filepath)
    print len(im), len(im[0])
    backproj = c.detect(im)
    rescaled = backproj/numpy.max(backproj) * 255
#    for i in range(750):
#      rescaled[i,:] = rescaled[i,:] * 0
#    thresholded = recog.thresholdImage(backproj, 127)
    outfile = "C:/Users/Moon/Desktop/Summer Research/TACOS/pics/hands/track%d.jpg" % count
    cv2.imwrite(outfile, rescaled)
# 
#  cv2.imshow("BACKPROJ",backproj/numpy.max(backproj))
#  cv2.waitKey()


##############
main()