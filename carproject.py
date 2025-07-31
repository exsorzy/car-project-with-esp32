from machine import Pin, PWM, time_pulse_us
from time import sleep
import math

IN1 = Pin(25, Pin.OUT)
IN2 = Pin(26, Pin.OUT)
IN3 = Pin(17, Pin.OUT)
IN4 = Pin(16, Pin.OUT)

TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

servo = PWM(Pin(19), freq=50)

LEFT_ANGLE = 180
CENTER_ANGLE = 90
RIGHT_ANGLE = 0

SAFE_DISTANCE = 15

def forward():
    IN1.on(); IN2.off()
    IN3.on(); IN4.off()

def backward():
    IN1.off(); IN2.on()
    IN3.off(); IN4.on()

def stop():
    IN1.off(); IN2.off()
    IN3.off(); IN4.off()

def turn_left():
    IN1.off(); IN2.on()
    IN3.on(); IN4.off()
    sleep(0.5)
    stop()

def turn_right():
    IN1.on(); IN2.off()
    IN3.off(); IN4.on()
    sleep(0.5)
    stop()

def set_servo_angle(angle):
    duty = int((angle / 180) * 102 + 26)
    servo.duty(duty)
    sleep(0.5)

def get_distance():
    TRIG.off()
    sleep(0.002)
    TRIG.on()
    sleep(0.00001)
    TRIG.off()
    pulse = time_pulse_us(ECHO, 1, 30000)
    distance = (pulse / 2) / 29.1
    return distance if distance < 400 else 400

set_servo_angle(CENTER_ANGLE)

try:
    while True:
        dist = get_distance()
        print("Distance:", dist, "cm")

        if dist > SAFE_DISTANCE:
            forward()
        else:
            stop()
            print("Obstacle detected! Scanning...")

            set_servo_angle(LEFT_ANGLE)
            sleep(0.5)
            left_dist = get_distance()
            print("Left:", left_dist, "cm")

            set_servo_angle(RIGHT_ANGLE)
            sleep(0.5)
            right_dist = get_distance()
            print("Right:", right_dist, "cm")

            set_servo_angle(CENTER_ANGLE)

            if left_dist > SAFE_DISTANCE and left_dist >= right_dist:
                print("Turning LEFT")
                turn_left()
            elif right_dist > SAFE_DISTANCE:
                print("Turning RIGHT")
                turn_right()
            else:
                print("No clear path! Reversing...")
                backward()
                sleep(0.5)
                stop()

except KeyboardInterrupt:
    print("\nProgram stopped with Ctrl+C")
    stop()

