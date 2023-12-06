import rclpy
import cv2 as cv
import time
import numpy as np
import CommandPublisher
import ImageSubscriber
import USSubscriber
import os

class BotCommands:
    def __init__(self):
        self.camResolutionX = 640
        self.camResolutionY = 640

        self.oneMeterDistanceInPixels = 100 # TODO: get the real measurement
        self.ballWidthMm = 65
        self.ballWidth1MeterInPixels = 50 # TODO: get the real measurement
        self.angleAtEdgeOfCameraFOV = 45 # TODO: get the real measurement
        self.acceptableCenterAngle = 10 # TODO: get the real measurement

    # unimplemented things
    def checkYOLOandUltrasonic(self):
        # return 0,0,0,0 if the ball is found by the ultrasonic
        return {} # ?

    def sendMessage(self, message):
        rclpy.init(args=None)
        node = CommandPublisher(message)

        rclpy.spin(node)

        # fire up reply subscriber
        # wait for state to change to ready
        
        # TODO: commandPublisher.publishCommand?
        # wait until once the robot replies that it recieved the message



    # unfinished things
    def waitForRobot(self):
        waiting = True
        print('waiting for robot')

        self.sendMessage({
            'command' : 'ready'
        })

    def getPosFromCoords(self, coords):
        # guess distance and angle here
        # return a dict with both values
        # TODO: correct labeled constants to reflect actual geometry
        furtherThan1Meter = coords['BL']['x'] >= self.oneMeterDistanceInPixels
        if furtherThan1Meter:
            distance = 1000
        else:
            ratio = self.oneMeterDistanceInPixels / coords['BL']['x'] # simple and imprecise
            distance = 1000 * ratio

        left = coords['BL']['y']
        right = coords['BR']['y']

        mid = (right + left) / 2

        camCenter = self.camResolutionY / 2

        angle = camCenter - mid

        if np.abs(angle) <= self.acceptableCenterAngle:
            angle = 0

        return {'distance' : distance, 'angle' : angle}





    # possibly finished things
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

    def commandToSearch(self, ballCoords, goalCoords):
        print('commanding robot to search, waiting for reply')
        reply = self.sendMessage({
            'command' : 'search'
        })
        print('reply recieved, evaluating data')
        self.checkYOLOandUltrasonic(reply)
        print('data processed')

    def hasItem(self, coords):
        if coords['TL'] == None:
            return False
        return True

