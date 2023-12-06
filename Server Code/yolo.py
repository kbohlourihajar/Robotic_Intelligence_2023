from ultralytics import YOLO
import cv2
import time

model = YOLO("C:/Users/kpche/OneDrive/Desktop/cs5510/runs/detect/train8/weights/best.onnx")

# Open the webcam
cap = cv2.VideoCapture(0)

while True:

    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break
    # Predict using the YOLO model
    results = model.predict(frame)

    for result in results:
        print(type(result.boxes.cls))
        print(result.boxes.xywh)

    time.sleep(1)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()

'''
def yoloView(frame):
    items = []
    results = model.predict(frame)
    for result in results:
        items.append(getPos(result))
    
    return items

def getPos(result):
    item {'size'}
    results.boxes.xywh[0]
'''

'''
#XYWH
results = model.predict('y.jpg')
for result in results:
    print(result.boxes.cls[0].item())
    print(result.boxes.xywh[0][0].item())
'''