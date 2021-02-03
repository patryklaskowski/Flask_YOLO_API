# __init__.py

import yaml
import time
import colorsys
import random
import cv2
import numpy as np


def load_yaml(path):
    with open(path) as file:
        output = yaml.safe_load(file)
    return output


def singleton(class_):
    instances = {}
    def wrapper(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return wrapper


def timer(func):
    '''
    Measure function runtime.
    ______
    INPUT:
    func: function
    ______
    RETURNS:
    {'result': result, 'time': elapsed_time}
    ______
    '''
    def inner_function(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        stop = time.perf_counter()
        elapsed_time = round(stop - start, 4)
        return {'result': result, 'time': elapsed_time}
    return inner_function


def dict_keys_to_int(dictionary):
    '''Change dictionary keys type to int.'''
    return {int(key):val for key, val in dictionary.items()}


def draw_bboxes(image, bboxes, classes=None, show_label=True):
    '''Draw predicted bounding boxes.'''
    classes = dict_keys_to_int(classes)
    image = image.copy()
    num_classes = len(classes)
    image_h, image_w, *_ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)

    out_boxes, out_scores, out_classes, num_boxes = bboxes
    for i in range(num_boxes[0]):
        if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > num_classes: continue
        coor = out_boxes[0][i].copy()
        coor[0] = int(coor[0] * image_h)
        coor[2] = int(coor[2] * image_h)
        coor[1] = int(coor[1] * image_w)
        coor[3] = int(coor[3] * image_w)

        fontScale = 0.5
        score = out_scores[0][i]
        class_ind = int(out_classes[0][i])
        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (coor[1], coor[0]), (coor[3], coor[2])
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

        if show_label:
            bbox_mess = '%s: %.2f' % (classes[class_ind], score)
            t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick // 2)[0]
            c3 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
            cv2.rectangle(image, c1, (np.float32(c3[0]), np.float32(c3[1])), bbox_color, -1) #filled

            cv2.putText(image, bbox_mess, (c1[0], np.float32(c1[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)
    return image
