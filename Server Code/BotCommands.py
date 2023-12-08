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
import copy

class BotCommands:
    def __init__(self):        
        rclpy.init(args=None)
        self.camResolutionX = 640
        self.camResolutionY = 640
        self.meters_per_sec = 0.56
        self.degrees_per_sec = 45

        self.oneMeterDistanceInPixels = 100 # TODO: get the real measurement
        self.ballWidthMm = 65
        self.ballWidth1MeterInPixels = 50 # TODO: get the real measurement
        self.angleAtEdgeOfCameraFOV = 45 # TODO: get the real measurement
        self.acceptableCenterAngle = 10 # TODO: get the real measurement
        self.commandNode = CommandPublisher.CommandPublisher()
        self.imageNode = ImageSubscriber.ImageSubscriber()
        self.ultrasonicNode = USSubscriber.USSubscriber()





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


        print('reply received, evaluating data')
        angleMod = -36
        for i in range(3):
            self.sendMessage({
                'command' : 'search',
                'angle' : 90 + angleMod
            })
        
            listOfItems = self.imageNode.process_latest_img()
            for j in listOfItems:
                if j['type'] == 'blueBall':
                    if posDict['ball'] == None:
                        angle = copy.deepcopy(j['x_angle'])
                        angle += angleMod
                        posDict['ball'] = {
                            'distance' : j['distance'],
                            'angle' : angle
                        }
                elif j['type'] == 'chessBoard':
                    angle = j['x_angle']
                    angle += angleMod
                    posDict['goal'] = {
                        'distance' : j['distance'],
                        'angle' : angle
                    }
            angleMod += 36

        return posDict
    
    
    def sendMessage(self, message):
        self.commandNode.publish_command(message)

        time.sleep(0.5)

    def driveBot(self, dist):
        print('commanding bot to drive forward, waiting for reply')
        self.sendMessage({
            'command' : 'drive',
            'amount' : dist / self.meters_per_sec
        })
        print('success')

    def rotateBot(self, angle):
        print('commanding bot to rotate, waiting for reply')
        self.sendMessage({
            'command' : 'rotate',
            'amount' : angle / self.degrees_per_sec
        })
        print('success')

    def search(self):
        print('commanding robot to search, waiting for reply')
        locations = self.checkYOLOandUltrasonic()
        print('data processed')

        return locations
