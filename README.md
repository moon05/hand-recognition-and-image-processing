# hand-recognization-and-image-processing

These are some of the scripts I wrote while I was working on Image Processing
as part of my summer research internship at University of Rochester.
This was used on the TACOS corpus. We wanted to track the hands in the cooking
videos, so we first labled all the hands from couple frames from each video and
then used the contours to track them. The result wasn't that good, there was a
lot of noise so we implemented a Background Subtractor on the tracks, which is
basically a Gaussian Mixture Model, which got rid of a lot of the noise and we 
were also able to track the faces without any labeling. In order to decrease
noise more, we did a morphological opening on the subtracted images, which gave
us way better images of hands. Ultimately the outputs are masks.

Libraries Needed: OpenCV, Numpy
