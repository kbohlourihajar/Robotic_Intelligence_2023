from ultralytics import YOLO
import cv2
import time

Horizontal_FOV = 52.8844060937 #degrees (0.9230070092945282) Radidans
Vertical_FOV = 41.2941180858 #degrees (0.7207183223027605) Radians
CHESSBOARD_METER = 0.18050996959209442
BLUEBALL_METER = 0.08107323944568634
YELLOWBALL_METER = 0.08612402528524399


model = YOLO("C:/Users/kpche/OneDrive/Desktop/cs5510/runs/detect/train8/weights/best.onnx")

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
        return {'distance': BLUEBALL_METER/max(w, h), 'x_angle': x_angle(x), 'y_angle': y_angle(y), 'type': 'blueBall'}
    if(result.boxes.cls[index].item() == 1):
        return {'distance': CHESSBOARD_METER/max(w, h), 'x_angle': x_angle(x), 'y_angle': y_angle(y), 'type': 'chessBoard'}
    if(result.boxes.cls[index].item() == 2):
        return {'distance': YELLOWBALL_METER/max(w, h), 'x_angle': x_angle(x), 'y_angle': y_angle(y), 'type': 'yellowBall'}
    else:
        return {'distance': -1, 'x': -1, 'y': -1, 'type': 'none'}

def x_angle(x):
    return (x-0.5)*Horizontal_FOV

def y_angle(y):
    return (y-0.5)*Vertical_FOV

#im_cv = cv2.imread("meter.png")
#im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
#scale_info = yoloView(im_rgb)
scale_info = yoloView("y.jpg")

for item in scale_info:
    print(item)


'''
  X-------->
Y    
|
|
|
V
'''

'''
#XYWH
results = model.predict('y.jpg')
for result in results:
    print(result.boxes.cls[0].item())
    print(result.boxes.xywh[0][1].item())
    print(result.boxes.cls)
    print(result.boxes.xywh)
'''
