from ultralytics import YOLO
import cv2
import time

Horizontal_FOV = 52.8844060937 #degrees (0.9230070092945282) Radidans
Vertical_FOV = 41.2941180858 #degrees (0.7207183223027605) Radians
CHESSBOARD_METER = 0.18050996959209442
BLUEBALL_METER = 0.08107323944568634
YELLOWBALL_METER = 0.08612402528524399

#Yolo model location
model = YOLO("best.onnx")


#Function to pass CV2 Image
#Returns a list of dictionaries with every detected object, its classification, and its relative location
def yoloView(frame):
    items = []
    results = model.predict(frame)

    if not results:
        return items
    for i in range(len(results[0].boxes.cls)):
        items.append(getPos(results[0], i))

    return items

#internal function to calculate information about a detected object
def getPos(result, index):
    x = result.boxes.xywhn[index][0].item()
    y = result.boxes.xywhn[index][1].item()
    w = result.boxes.xywhn[index][2].item()
    h = result.boxes.xywhn[index][3].item()
    if(result.boxes.cls[index].item() == 0):
        return {'distance': BLUEBALL_METER/min(w, h), 'x_angle': x_angle(x), 'y_angle': y_angle(y), 'type': 'blueBall', 'confidence': result.boxes.conf[index].item()}
    if(result.boxes.cls[index].item() == 1):
        return {'distance': CHESSBOARD_METER/min(w, h), 'x_angle': x_angle(x), 'y_angle': y_angle(y), 'type': 'chessBoard', 'confidence': result.boxes.conf[index].item()}
    if(result.boxes.cls[index].item() == 2):
        return {'distance': YELLOWBALL_METER/max(w, h), 'x_angle': x_angle(x), 'y_angle': y_angle(y), 'type': 'yellowBall', 'confidence': result.boxes.conf[index].item()}
    else:
        return {'distance': -1, 'x': -1, 'y': -1, 'type': 'none'}

#Functions to calculate angle of object based on its position seen by the camera 
def x_angle(x):
    return (x-0.5)*Horizontal_FOV

def y_angle(y):
    return (y-0.5)*Vertical_FOV



#For Model Testing reads an image from a file and returns the calculated information
if __name__ == "__main__":
    scale_info = yoloView("y.jpg")
    for item in scale_info:
        print(item)

'''
0.0 -> 1.0
  X-------->
Y    
|
|
|
V
'''
