import numpy as np
from numpy.core.fromnumeric import sort

from .yolov3.config import yolov3_config_voc as cfg
from .yolov3.eval.evaluator import Evaluator
from .yolov3.utils.tools import *
from .yolov3.utils.visualize import *


class Tester(object):
    def __init__(self,
                 model,
                 img=None,
                 ):

        self.__img = img
        self.__classes = cfg.DATA["CLASSES"]
        self.__model = model
        self.__evaluator = Evaluator(self.__model)

    def test(self):

        bboxes_prd = self.__evaluator.get_bbox(self.__img)
        if bboxes_prd.shape[0] != 0:
            boxes = bboxes_prd[..., :4]
            class_inds = bboxes_prd[..., 5].astype(np.int32)
            scores = bboxes_prd[..., 4]

            pred_img = visualize_boxes(image=self.__img, boxes=boxes, labels=class_inds,
                                       probs=scores, class_labels=self.__classes)

            sorted_ind = np.argsort(-scores)
            scores = scores[sorted_ind]
            class_inds = class_inds[sorted_ind]

            predicted = []
            probs = []

            for score, class_ind in zip(scores, class_inds):
                if score > 0.5:
                    predicted.append(class_ind)
                    probs.append(score)

        return pred_img, predicted, probs
