import argparse
import os

import torch

from .yolov3.config import yolov3_config_voc as cfg
from .yolov3.eval.evaluator import Evaluator
from .yolov3.model.yolov3_s import Yolov3_S
from .yolov3.utils.tools import *
from .yolov3.utils.visualize import *


class Tester(object):
    def __init__(self,
                 weight_path=None,
                 img_size=544,
                 img=None,
                 ):
        self.img_size = img_size
        self.__num_class = cfg.DATA["NUM"]
        self.__conf_threshold = cfg.TEST["CONF_THRESH"]
        self.__nms_threshold = cfg.TEST["NMS_THRESH"]
        self.__device = torch.device('cpu')
        self.__multi_scale_test = cfg.TEST["MULTI_SCALE_TEST"]
        self.__flip_test = cfg.TEST["FLIP_TEST"]

        self.__img = img
        self.__classes = cfg.DATA["CLASSES"]

        self.__model = Yolov3_S().to(self.__device)

        self.__load_model_weights(weight_path)

        self.__evaluator = Evaluator(self.__model, visiual=False)

    def __load_model_weights(self, weight_path):
        # print("loading weight file from : {}".format(weight_path))

        weight = os.path.join(weight_path)
        chkpt = torch.load(weight, map_location=self.__device)
        self.__model.load_state_dict(chkpt)
        # print("loading weight file is done")
        del chkpt

    def test(self):
        path = self.__img
        # print("test images : {}".format(path))

        img = cv2.imread(path)
        assert img is not None

        bboxes_prd = self.__evaluator.get_bbox(img)
        if bboxes_prd.shape[0] != 0:
            boxes = bboxes_prd[..., :4]
            class_inds = bboxes_prd[..., 5].astype(np.int32)
            scores = bboxes_prd[..., 4]

            visualize_boxes(image=img, boxes=boxes, labels=class_inds,
                            probs=scores, class_labels=self.__classes)
            path = os.path.join(
                cfg.PROJECT_PATH, "data/{}".format(img))

            cv2.imwrite(path, img)
            print("saved images : {}".format(path))


if __name__ == "__main__":
    Tester(weight_path="static/weights.pt", img="path_to_image").test()
