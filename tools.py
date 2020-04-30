import copy
import cv2
import math

"""
Collection of tools handling bounding-boxes
"""

def nms(orig_dets, iou_thresh):
    """
    :param dets: [[x, y, w, h], ..., [x, y, w, h]]
    :return: keeping det indices
    """

    dets = copy.deepcopy(orig_dets)
    dets = dets[dets[:,5].argsort()[::-1]]
    keep = [True]*len(dets)
    for i in range(0, len(dets)-1):
        for j in range(i+1, len(dets)):
            if iou(dets[i], dets[j]) > iou_thresh:
                keep[j] = False
    print(keep)
    return keep

def iou(bb1, bb2):
    x1 = max(bb1[0], bb2[0])
    y1 = max(bb1[1], bb2[1])
    x2 = min(bb1[0]+bb1[2], bb2[0]+bb2[2])
    y2 = min(bb1[1]+bb1[3], bb1[1]+bb2[3])

    intersection = max(0, x2-x1+1)*max(0, y2-y1+1)

    bb1_area = bb1[2]*bb1[3]
    bb2_area = bb2[2]*bb2[3]

    iou = intersection/float(bb1_area + bb2_area - intersection)

    return iou


def separate_measure(bb1, bb2):
    cpos1 = [bb1[0]+bb1[2]/2, bb1[1]+bb1[3]/2]
    cpos2 = [bb2[0]+bb2[2]/2, bb2[1]+bb2[3]/2]

    pos_dist = math.sqrt((cpos1[0]-cpos2[0])**2 + (cpos1[1]-cpos2[1])**2)
    shp_dist = min(bb1[3]/bb2[3], bb2[3]/bb1[3])

    return pos_dist, shp_dist


def normalization(img):
    norm_img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    return norm_img