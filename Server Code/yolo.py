from ultralytics import YOLO
import cv2
import time

model = YOLO("best.onnx")

def yoloView(frame):
    items = []
    results = model.predict(frame)
    if not results: # check if nothing is seen
        return items
    for result in results: #loop through every seen item
        items.append(getPos(result))
    
    return items

def getPos(result)
    x = result.boxes.xywh[0][0].item()
    y = result.boxes.xywh[0][1].item()
    w = result.boxes.xywh[0][2].item()
    h = result.boxes.xywh[0][3].item()
    if(print(result.boxes.cls[0].item()) = 0):
        return {'size': (w+h)/2 'x': x+w/2, 'y': y+h/2, 'type': 'blueBall'}
    if(print(result.boxes.cls[1].item()) = 0):
        return {'size': (w+h)/2 'x': x+w/2, 'y': y+h/2, 'type': 'chessBoard'}
    if(print(result.boxes.cls[2].item()) = 0):
        return {'size': (w+h)/2 'x': x+w/2, 'y': y+h/2, 'type': 'yellowBall'}
    else:
        return {'size': -1 'x': -1, 'y': -1, 'type': 'none'}
        
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
