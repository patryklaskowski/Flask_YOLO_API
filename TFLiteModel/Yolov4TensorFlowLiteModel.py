# Yolov4TensorFlowLiteModel.py

import tensorflow as tf
import cv2
import numpy as np


class Yolov4TensorFlowLiteModel:
    '''
    Parameters
    ----------
    model_path : path
        Path to .tflite file.
    names_path : path
        Path to .names file corresponding to provided model.
    '''

    def __init__(self, model_path, names_path):
        self.model_path = model_path
        self.names_path = names_path
        self.classes = self.__read_class_names(names_path)
        self.num_class = len(self.classes)
        self.__startup_session()


    def __repr__(self):
        return f'Yolov4TensorFlowLiteModel({self.model_path}, {self.names_path}, {self.treshold}, {self.iou})'


    def __read_class_names(self, path):
        '''Reads class names from file.'''
        names = {}
        with open(path) as file:
            for ID, name in enumerate(file):
                names[ID] = name.strip('\n')
        return names


    def __startup_session(self):
        '''Builds model from file.'''
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()[0]
        self.output_details = self.interpreter.get_output_details()
        *_, height, width, depth = self.input_details['shape']
        assert height == width, 'Height and width must be equal.'
        self.input_size = height


    def predict(self, image, treshold=0.4, iou=0.5):
        image = cv2.resize(image, (self.input_size, self.input_size))
        image = image / 255.
        image = image[np.newaxis, ...].astype(np.float32)
        ### Input
        self.interpreter.set_tensor(self.input_details['index'], image)
        ### Forward propagation
        self.interpreter.invoke()
        ### Output
        output = [self.interpreter.get_tensor(self.output_details[i]['index']) for i in range(len(self.output_details))]
        boxes, scores, *_ = output
        boxes, pred_conf = self.__filter_boxes(boxes, scores, treshold)
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes = tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores = tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class = 50,
            max_total_size = 50,
            iou_threshold = iou,
            score_threshold = treshold,
        )
        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]

        return pred_bbox


    def __filter_boxes(self, box_xywh, scores, treshold):
        input_shape = tf.constant([self.input_size, self.input_size])
        # Max value over multiple rows
        scores_max = tf.math.reduce_max(scores, axis=-1)
        mask = scores_max >= treshold
        class_boxes = tf.boolean_mask(box_xywh, mask)
        pred_conf = tf.boolean_mask(scores, mask)
        class_boxes = tf.reshape(class_boxes, [tf.shape(scores)[0], -1, tf.shape(class_boxes)[-1]])
        pred_conf = tf.reshape(pred_conf, [tf.shape(scores)[0], -1, tf.shape(pred_conf)[-1]])

        box_xy, box_wh = tf.split(class_boxes, (2, 2), axis=-1)

        input_shape = tf.cast(input_shape, dtype=tf.float32)

        box_yx = box_xy[..., ::-1]
        box_hw = box_wh[..., ::-1]

        box_mins = (box_yx - (box_hw / 2.)) / input_shape
        box_maxes = (box_yx + (box_hw / 2.)) / input_shape

        boxes = tf.concat([
            box_mins[..., 0:1],  # y_min
            box_mins[..., 1:2],  # x_min
            box_maxes[..., 0:1],  # y_max
            box_maxes[..., 1:2]  # x_max
        ], axis=-1)

        return (boxes, pred_conf)
