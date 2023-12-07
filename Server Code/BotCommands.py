import rclpy
import cv2 as cv
import time
import numpy as np
import CommandPublisher
import ImageSubscriber
import USSubscriber
import StateSubscriber
import os
import yolo

class BotCommands:
    def __init__(self):        
        rclpy.init(args=None)
        self.camResolutionX = 640
        self.camResolutionY = 640

        self.oneMeterDistanceInPixels = 100 # TODO: get the real measurement
        self.ballWidthMm = 65
        self.ballWidth1MeterInPixels = 50 # TODO: get the real measurement
        self.angleAtEdgeOfCameraFOV = 45 # TODO: get the real measurement
        self.acceptableCenterAngle = 10 # TODO: get the real measurement
        self.commandNode = CommandPublisher.CommandPublisher()
        self.imageNode = ImageSubscriber.ImageSubscriber()
        self.ultrasonicNode = USSubscriber.USSubscriber()
        self.stateNode = StateSubscriber.StateSubscriber()

    # unimplemented things
    def getPics(self):
        # figure out how to aquire pics for yolo
        return





    # unfinished things
    def waitForRobot(self):
        print('waiting for robot')

        self.sendMessage({
            'command' : 'ready'
        })




    # possibly finished things
    def checkYOLOandUltrasonic(self):
        # {'distance': BLUEBALL_METER/max(w, h), 'x_angle': x_angle(x), 'y_angle': y_angle(y), 'type': 'blueBall'}

        posDict = {
            'ball' : None,
            'goal' : None
        }

        # check ultrasonic
        readings = []
        for i in range(10):
            rclpy.spin_once(self.ultrasonicNode)
            readings.append(self.ultrasonicNode.getFeedback())
        avgFeedback = np.mean(readings)
        if avgFeedback < 10:
            posDict['ball'] = {
                'distance' : 0,
                'angle' : 0
            }
        
        pictures = self.getPics()
        
        angleMod = -36
        for pic in pictures:
            listOfItems = yolo.yoloView(pic)

            for i in listOfItems:
                if i['type'] == 'blueBall':
                    if posDict['ball'] == None:
                        angle = i['x_angle']
                        angle += angleMod
                        posDict['ball'] = {
                            'distance' : i['distance'],
                            'angle' : angle
                        }
                elif i['type'] == 'chessBoard':
                    angle = i['x_angle']
                    angle += angleMod
                    posDict['goal'] = {
                        'distance' : i['distance'],
                        'angle' : angle
                    }
            angleMod += 36

        return posDict
    
    
    def sendMessage(self, message):
        self.commandNode.publish_command(message)

        time.sleep(.5)

        while(self.stateNode.getState != 'ready'): # check if it's ready
            rclpy.spin_once(self.stateNode)


    def driveBot(self, dist):
        print('commanding bot to drive forward, waiting for reply')
        self.sendMessage({
            'command' : 'drive',
            'amount' : dist
        })
        print('success')

    def rotateBot(self, angle):
        print('commanding bot to rotate, waiting for reply')
        self.sendMessage({
            'command' : 'rotate',
            'amount' : angle
        })
        print('success')

    def search(self):
        print('commanding robot to search, waiting for reply')
        reply = self.sendMessage({
            'command' : 'search'
        })
        if len(os.listdir('./imgBuffer')) >= 3:
            print('reply recieved, evaluating data')
            locations = self.checkYOLOandUltrasonic(reply)
            print('data processed')
            for i in os.listdir('./imgBuffer'):
                os.remove(i)
        else:
            raise Exception('image buffer chcked, but returned empty')
        return locations
