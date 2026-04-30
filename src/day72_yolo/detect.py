from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "yolov8n.pt"
INPUT_IMAGE = BASE_DIR / "traffic.jpg"
OUTPUT_IMAGE = BASE_DIR / "output.jpg"


def main() -> int:
    try:
        import cv2
    except ModuleNotFoundError:
        print(
            "Missing dependency: opencv-python. Install it with:\n"
            "  pip install -r requirements.txt"
        )
        return 1

    try:
        from ultralytics import YOLO
    except ModuleNotFoundError:
        print(
            "Missing dependency: ultralytics. Install it with:\n"
            "  pip install -r requirements.txt"
        )
        return 1

    if not MODEL_PATH.exists():
        print(f"Model file not found: {MODEL_PATH}")
        return 1

    if not INPUT_IMAGE.exists():
        print(f"Input image not found: {INPUT_IMAGE}")
        return 1

    model = YOLO(str(MODEL_PATH))
    results = model(str(INPUT_IMAGE))
    img = results[0].plot()

    if not cv2.imwrite(str(OUTPUT_IMAGE), img):
        print(f"Failed to write output image: {OUTPUT_IMAGE}")
        return 1

    print(f"Output saved as {OUTPUT_IMAGE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
