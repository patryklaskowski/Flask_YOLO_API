# model.

from .Yolov4TensorFlowLiteModel import Yolov4TensorFlowLiteModel
import yaml

with open('cfg.yaml') as file:
    cfg = yaml.safe_load(file)

model_path = cfg['model_path']
names_path = cfg['names_path']

yolov4 = Yolov4TensorFlowLiteModel(model_path, names_path)
