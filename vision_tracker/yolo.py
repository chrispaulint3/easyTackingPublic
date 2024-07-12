import cv2
from ultralytics import YOLO


def yolo_track_frame(image_stream):
    model = YOLO("./models/yolov8n.pt")
    # for frame in image_stream:
    #     results = model.track(frame,persist=True)
    #     annotated_frame = results[0].plot()
    #     cv2.imshow("yolo_detect",annotated_frame)
    #     if cv2.waitKey(1) & 0xFF == ord("q"):
    #         break

yolo_track_frame("tes")