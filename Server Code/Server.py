import cv2 as cv
import time
import numpy as np
import BotCommands

angle_tolerance = 10

if __name__ == '__main__':
    bot = BotCommands.BotCommands()
    

    running = True

    goalRelativeAngle = None

    while running:
        ballCoords = {} # bounding box
        goalCoords = {} # ditto
        locations = bot.search()
        if locations['ball'] != None: # sees ball
            print('found ball')            
            ballSpot = locations['ball']
            if locations['goal'] != None: # sees goal
                print('and goal')
                goalSpot = locations['goal']
                if goalSpot['distance'] < 0.35 and ballSpot['distance'] == 0: # posesses ball in goal
                    print('bot has delivered the package')
                    bot.sendMessage({
                        'command' : 'celebrate'
                    })
                    running = False
                elif np.abs(goalSpot['angle']) < angle_tolerance and np.abs(ballSpot['angle']) < angle_tolerance: # goal and ball are lined up, posess and not posessed
                    bot.driveBot(goalSpot['distance'])
                elif goalSpot['angle'] > 0 and ballSpot['distance'] == 0: # posesses ball outside of goal, not lined up
                    bot.rotateBot(goalSpot['angle'])
                elif ballSpot['distance'] > 0 and np.abs(ballSpot['angle']) < angle_tolerance: # does not posess ball, outside goal, lined up
                    goalRelativeAngle = goalSpot['angle']
                    bot.driveBot(ballSpot['distance'])
                elif np.abs(ballSpot['angle']) > angle_tolerance: # does not possess ball, outside goal, not lined up
                    goalRelativeAngle = goalSpot['angle']
                    bot.rotateBot(ballSpot['angle'])
                else: # if I missed a scenario
                    print('failed at sees ball and goal')
            else: # sees ball not goal
                if goalRelativeAngle != None and ballSpot['distance'] == 0: # has ball and has seen goal
                    bot.rotateBot(goalRelativeAngle)
                    goalRelativeAngle = None
                elif goalRelativeAngle == None and ballSpot['distance'] == 0: # has ball and hasn't seen goal
                    bot.rotateBot(160)
                elif np.abs(ballSpot['angle']) < angle_tolerance and ballSpot['distance'] != 0: # does not have ball, lined up
                    bot.driveBot(ballSpot['distance'])
                elif np.abs(ballSpot['angle']) > angle_tolerance and ballSpot['distance'] != 0: # does not have ball, not lined up
                    bot.rotateBot(ballSpot['angle'])
                    if goalRelativeAngle != None:
                        goalRelativeAngle += ballSpot['angle']
                else: # if I missed a situation
                    print('failed at sees ball not goal')
                    

        elif locations['goal'] != None: # sees goal not ball
            print('found goal')
            goalRelativeAngle = locations['goal']['angle']
            bot.rotateBot(120)
            goalRelativeAngle += 120
        else: # sees neither
            print('found nothing')
            bot.rotateBot(120) # spin around if nothing found

            







        


