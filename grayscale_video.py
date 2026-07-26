import argparse
from pathlib import Path

import cv2


def convert_to_grayscale(input_video: str, output_video: str) -> None:
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {input_video}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_path = Path(output_video)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    if not out.isOpened():
        raise RuntimeError("Could not create output video writer.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))

    cap.release()
    out.release()
    print(f"Saved grayscale video to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a video to grayscale")
    parser.add_argument("input_video", help="Path to the input video")
    parser.add_argument(
        "output_video",
        nargs="?",
        default="output_grayscale.mp4",
        help="Optional output video path",
    )
    args = parser.parse_args()
    convert_to_grayscale(args.input_video, args.output_video)
