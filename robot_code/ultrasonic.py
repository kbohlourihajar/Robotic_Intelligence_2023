import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

EchoPin = 18
TrigPin = 16
BuzzerPin = 32

GPIO.setmode(GPIO.BOARD)

GPIO.setup(BuzzerPin, GPIO.OUT)
GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(TrigPin, GPIO.OUT)

theremin = False

if theremin:
	p = GPIO.PWM(32, 440)
	p.start(50)

def distance():
	GPIO.output(TrigPin, GPIO.LOW)
	time.sleep(0.000002)
	GPIO.output(TrigPin, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TrigPin, GPIO.LOW)

	t3 = time.time()

	while not GPIO.input(EchoPin):
		t4 = time.time()
		if (t4 - t3 > 0.03):
			return -1
	t1 = time.time()
	while GPIO.input(EchoPin):
		t5 = time.time()
		if (t5 - t1) > 0.03:
			return -1

	t2 = time.time()
	time.sleep(0.01)
	return ((t2 - t1) * 340 / 2) * 100

if __name__ == '__main__':
	while(theremin):
		time.sleep(0.1)
		p.ChangeFrequency(distance() * 15)
