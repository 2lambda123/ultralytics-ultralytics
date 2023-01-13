# Ultralytics YOLO 🚀, GPL-3.0 license

from ultralytics.yolo.configs import get_config
from ultralytics.yolo.utils import DEFAULT_CONFIG, ROOT
from ultralytics.yolo.v8 import classify, detect, segment
CFG_DET = 'yolov8n.yaml'
CFG_SEG = 'yolov8n-seg.yaml'
CFG_CLS = 'squeezenet1_0'
CFG = get_config(DEFAULT_CONFIG)
SOURCE = ROOT / "assets"


def test_detect():
    overrides = {"data": "coco8.yaml", "model": CFG_DET, "imgsz": 32, "epochs": 1, "save": False}
    CFG.data = "coco8.yaml"

    # Trainer
    trainer = detect.DetectionTrainer(overrides=overrides)
    trainer.train()
    trained_model = trainer.best

    # Validator
    val = detect.DetectionValidator(args=CFG)
    val(model=trained_model)

    # Predictor
    pred = detect.DetectionPredictor(overrides={"imgsz": [64, 64]})
    result = pred(source=SOURCE, model="yolov8n.pt")
    assert len(result), "predictor test failed"

    overrides["resume"] = trainer.last
    trainer = detect.DetectionTrainer(overrides=overrides)
    try:
        trainer.train()
    except Exception as e:
        print(f"Expected exception caught: {e}")
        return

    Exception("Resume test failed!")


def test_segment():
    overrides = {"data": "coco8-seg.yaml", "model": CFG_SEG, "imgsz": 32, "epochs": 1, "save": False}
    CFG.data = "coco8-seg.yaml"
    CFG.v5loader = False
    # YOLO(CFG_SEG).train(**overrides)  # works

    # trainer
    trainer = segment.SegmentationTrainer(overrides=overrides)
    trainer.train()
    trained_model = trainer.best

    # Validator
    val = segment.SegmentationValidator(args=CFG)
    val(model=trained_model)

    # Predictor
    pred = segment.SegmentationPredictor(overrides={"imgsz": [64, 64]})
    result = pred(source=SOURCE, model="yolov8n-seg.pt")
    assert len(result) == 2, "predictor test failed"

    # Test resume
    overrides["resume"] = trainer.last
    trainer = segment.SegmentationTrainer(overrides=overrides)
    try:
        trainer.train()
    except Exception as e:
        print(f"Expected exception caught: {e}")
        return

    Exception("Resume test failed!")


def test_classify():
    overrides = {"data": "mnist160", "model": "yolov8n-cls.yaml", "imgsz": 32, "epochs": 1, "batch": 64, "save": False}
    CFG.data = "mnist160"
    CFG.imgsz = 32
    CFG.batch = 64
    # YOLO(CFG_SEG).train(**overrides)  # works

    # Trainer
    trainer = classify.ClassificationTrainer(overrides=overrides)
    trainer.train()
    trained_model = trainer.best

    # Validator
    val = classify.ClassificationValidator(args=CFG)
    val(model=trained_model)

    # Predictor
    pred = classify.ClassificationPredictor(overrides={"imgsz": [64, 64]})
    result = pred(source=SOURCE, model=trained_model)
    assert len(result) == 2, "predictor test failed"
