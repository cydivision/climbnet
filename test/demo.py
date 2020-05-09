import os

import cv2
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import DatasetCatalog
from detectron2.data import MetadataCatalog
from detectron2.data.datasets import register_coco_instances
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import ColorMode
from detectron2.utils.visualizer import Visualizer


def run_inference(image_path, model_path):
    register_coco_instances("climb_dataset", {}, "./mask.json", "")

    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATALOADER.NUM_WORKERS = 1
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3  # 3 classes (hold, volume, downclimb)
    cfg.MODEL.WEIGHTS = os.path.join(model_path)
    cfg.MODEL.DEVICE = 'cpu'
    cfg.DATASETS.TEST = ("climb_dataset",)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.75  # set the testing threshold for this model

    # setup inference

    predictor = DefaultPredictor(cfg)
    train_metadata = MetadataCatalog.get("climb_dataset")

    # dataset catalog needs to exist so the polygon classes show up correctly
    DatasetCatalog.get("climb_dataset")
    im = cv2.imread(image_path)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=train_metadata,
                   scale=0.75,
                   instance_mode=ColorMode.IMAGE_BW  # remove the colors of unsegmented pixels
                   )
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imshow('climbnet', v.get_image()[:, :, ::-1])
    cv2.waitKey(0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Climbnet demo')
    parser.add_argument('image_path', type=str,
                        help='image file')
    parser.add_argument('model_path', type=str,
                        help='climbnet model weights')

    args = parser.parse_args()

    run_inference(args.image_path, args.model_path)
