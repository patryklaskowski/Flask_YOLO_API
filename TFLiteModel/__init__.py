# __init__.py

print('> ./TFLiteModel/__init__.py')

import tensorflow as tf
import cv2
import numpy as np

class Yolov4TensorFlowLiteModel:
    '''
    Convert the input to an array.

    Parameters
    ----------
    model_path : path
        Path to .tflite file.
    names_path : path
        Path to .names file corresponding to provided model.
    input_size : (temporary inactive) int
        Single number representing height and width of provided model input.
    treshold :  float
        Defaults to 0.2.
    iou : float
        Defaults to 0.4.
    '''

    def __repr__(self):
        return f'Yolov4TensorFlowLiteModel({self.model_path}, {self.names_path}, {self.treshold}, {self.iou})'

    def __init__(self, model_path, names_path, treshold=0.2, iou=0.4):
        self.model_path = model_path
        self.names_path = names_path
        # self.input_size = input_size
        self.treshold = treshold
        self.iou = iou
        self.classes = self.__read_class_names()
        self.num_class = len(self.classes)

        self.__startup_session()
        print(f'> TensorFlowLiteModel initialization success!')

        # Removed input_size from required attributes. This is test
        self.input_size = self.input_details[0]['shape'][1]


    def __read_class_names(self):
        '''
        Reads class names from file.
        '''
        names = {}
        with open(self.names_path) as file:
            for ID, name in enumerate(file):
                names[ID] = name.strip('\n')
        return names


    def __startup_session(self):
        '''
        Builds model from file.
        '''
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        input_details = self.input_details[0]
        print(f'> __startup_session.')
        print(f'> Expected input shape: {input_details["shape"]}.')
        print(f'> Expected input dtype: {input_details["dtype"]}.')


    def predict(self, frame):
        '''
        Performs object detection.

        Parameters
        ----------
        frame : array-like

        Returns
        -------
        bbox : array-like
        '''

        frame = cv2.resize(frame, (self.input_size, self.input_size))
        image_data = frame / 255. # Normalize
        image_data = image_data[np.newaxis, ...].astype(np.float32) # Creates a single batch shape: (1, input_size, input_size, channels)

        ### ALL THE MAGIC ###
        self.interpreter.set_tensor(self.input_details[0]['index'], image_data) # Put the input data on
        self.interpreter.invoke() # Forward
        pred = [self.interpreter.get_tensor(self.output_details[i]['index']) for i in range(len(self.output_details))] # Pick the outputs up
        #####################

        boxes, pred_conf = self.__filter_boxes(box_xywh=pred[0], scores=pred[1])

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes = tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores = tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class = 50,
            max_total_size = 50,
            iou_threshold = self.iou,
            score_threshold = self.treshold,
        )

        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]

        return pred_bbox


    def __filter_boxes(self, box_xywh, scores):
        input_shape = tf.constant([self.input_size, self.input_size])
        scores_max = tf.math.reduce_max(scores, axis=-1)
        mask = scores_max >= self.treshold
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
