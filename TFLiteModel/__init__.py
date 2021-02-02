# model.

from .yolo import Yolov4TensorFlowLiteModel
from utils import load_yaml

cfg = load_yaml('cfg.yaml')

model_path = cfg['model_path']
names_path = cfg['names_path']

yolov4 = Yolov4TensorFlowLiteModel(model_path, names_path)
