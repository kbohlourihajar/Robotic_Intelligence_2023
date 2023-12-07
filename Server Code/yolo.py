from ultralytics import YOLO
import cv2
import time

model = YOLO("best.onnx")

def yoloView(frame):
    items = []
    results = model.predict(frame)

    if not results:
        return items
    for i in range(len(results[0].boxes.cls)):
        items.append(getPos(results[0], i))
        
    return items

def getPos(result, index):
    x = result.boxes.xywhn[index][0].item()
    y = result.boxes.xywhn[index][1].item()
    w = result.boxes.xywhn[index][2].item()
    h = result.boxes.xywhn[index][3].item()
    if(result.boxes.cls[index].item() == 0):
        return {'size': max(w, h), 'x': x, 'y': y, 'type': 'blueBall'}
    if(result.boxes.cls[index].item() == 1):
        return {'size': w, 'x': x, 'y': y, 'type': 'chessBoard'}
    if(result.boxes.cls[index].item() == 2):
        return {'size': max(w, h), 'x': x, 'y': y, 'type': 'yellowBall'}
    else:
        return {'size': -1, 'x': -1, 'y': -1, 'type': 'none'}
        
'''
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

'''
#XYWH
results = model.predict('y.jpg')
for result in results:
    print(result.boxes.cls[0].item())
    print(result.boxes.xywh[0][0].item())
'''
