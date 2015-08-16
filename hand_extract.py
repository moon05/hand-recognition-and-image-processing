import recog
import compatcv
import cv2
import numpy
import sys
import lvutils
import camera

def get_lab_colorhist(colors, bins=16):
    hist = recog.colorHist(colors, [1, 2], conv=cv2.cv.CV_BGR2Lab, bins=bins)
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    return hist

def get_rgb_colorhist(colors, bins=16):
    hist = recog.colorHist(colors, [0, 1, 2], bins=bins)
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    return hist

def main(im, lab_hist, rgb_hist, bins=16, thresh=64, frame_no=0, save_image_path=None):
    slack = 10
    h, w = im.shape[:2]

    lab_retp = reorcog.detectColHist(im, lab_hist, [1, 2], conv=cv2.cv.CV_BGR2Lab, bins=bins).astype('uint8')
    rgb_retp = recog.detectColorHistBGR(im, rgb_hist, bins).astype('uint8')

    lab_thr = recog.thresholdImage(lab_retp, thresh)
    rgb_thr = recog.thresholdImage(rgb_retp, thresh)

    rev_thr_F = recog.thresholdImage(lab_retp, 32)
    rev_thr_F = recog.dilate(rev_thr_F, 10) 
    rev_thr_F = recog.invertImage(rev_thr_F)
    rev_thr_T = recog.thresholdImage(rgb_retp, thresh)

    lab_thr = recog.erode_dilate(lab_thr)
    rgb_thr = recog.erode_dilate(rgb_thr)

    ctrs = compatcv.createContours(lab_thr)
    if save_image_path != None:
        im2 = im
    for c in ctrs:
        msk = compatcv.createMask((h, w), [c])
        msk_overlap = numpy.minimum(msk, rgb_thr)
        if numpy.max(msk_overlap) > 0:
            ocvc = compatcv.convContoursO([c])[0]
            x1, y1, w1, h1 = cv2.boundingRect(ocvc)
            # large bounding box - hand candidate
            if w1*h1 > 500:
                # designate interest area (box)
                interest = numpy.zeros((h, w), dtype=numpy.uint8)
                cv2.rectangle(interest, (x1-slack, y1-slack), (x1+w1+slack, y1+h1+slack), 255, -1)

                # initialize
                maskgc = numpy.zeros((h, w), dtype=numpy.uint8)
                bgdmodel = numpy.zeros((1,65),numpy.float64)
                fgdmodel = numpy.zeros((1,65),numpy.float64)
                cv2.grabCut(im, maskgc, (x1-slack, y1-slack, w1+(slack*2), h1+(slack*2)), bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)

                # force high probability true and false pixels
                maskgc = numpy.where((rev_thr_T == 255), 1, maskgc)
                maskgc = numpy.where((rev_thr_F == 255), 0, maskgc)
                maskgc = numpy.minimum(interest, maskgc)

                # rerun with forced pixels
                cv2.grabCut(im, maskgc, (x1-slack, y1-slack, w1+(slack*2), h1+(slack*2)), bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_MASK)

                # get mask
                mask2 = numpy.where((maskgc==1) + (maskgc==3),255,0).astype('uint8')
                mask_ctr = compatcv.createContours(mask2)[0]
                if save_image_path != None:
                    cv2.drawContours(im2, compatcv.convContoursO([mask_ctr]), -1, (0, 0, 255), 2)

                    # interest area rectangle
                    cv2.rectangle(im2, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 1)

                print "L1", ",".join([str(k) for k in [x1, y1, w1, h1]])
                print "MASK",
                for coord in mask_ctr:
                    print str(coord[0])+","+str(coord[1]),
                print
            elif w1*h1 > 100:
                if save_image_path != None:
                    cv2.rectangle(im2, (x1, y1), (x1+w1, y1+h1), (0, 128, 0), 1)
                print "L2", ",".join([str(k) for k in [x1, y1, w1, h1]])

    if save_image_path != None:
        if save_image_path == "imshow":
            cv2.imshow('IM2', im2)
            cv2.waitKey(10)
        else:
            cv2.imwrite(save_image_path + "/out%06d.jpg" % frame_no, im2)

if __name__ == '__main__':
    save_image = None
    if len(sys.argv) == 4:
        pass
    elif len(sys.argv) == 5:
        save_image = sys.argv[4]
        pass
    else:
        print "Usage", sys.argv[0], "[path] [skip] [offset] (save_path|imshow)"
        exit()

    path = sys.argv[1] # /mnt/hd/uw/bioturk_3010-8279/protocol/ds40
    skip = int(sys.argv[2])
    offset = int(sys.argv[3])

    istc = camera.Stream(path)
    bins, thresh = 16, 64
    #colors = recog.read_asimg("hand_model.txt")
    #lab_hist = get_lab_colorhist(colors, bins)
    #rgb_hist = get_rgb_colorhist(colors, bins)
    p = lvutils.Pickle("hand_model.pkl")
    lab_hist, rgb_hist = p.load()

    try:
        while istc.getFrame():
            if istc.color_frame % skip == offset:
                sys.stderr.write("FRAME %d\n" % istc.color_frame)
                print "FRAME", istc.color_frame
                main(istc.color, lab_hist, rgb_hist, bins, thresh, istc.color_frame, save_image)
                sys.stderr.flush()
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass
