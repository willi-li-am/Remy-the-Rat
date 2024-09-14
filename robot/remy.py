from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time 

factory = PiGPIOFactory()
right_servo = Servo(17, pin_factory=factory) # we can change the pin numbers later
left_servo = Servo(27, pin_factory=factory)

left_servo_default_angle = 0
right_servo_default_angle = 0 # TODO: test this angle later 

def convert_angle_to_servo_value(angle): 
    return (angle - 90) / 90

# define some functions here, about remy's actions related to servo motors 

def chopping(time_needed): 
    curr_time = time.time() 
    end_time = curr_time + time_needed 
    while curr_time < end_time: 
        right_servo.value = convert_angle_to_servo_value(180) # TODO: figure out the value that it should move to here
        time.sleep(0.2)
        right_servo.value = convert_angle_to_servo_value(0)
        time.sleep(0.2)
        curr_time = time.time()
    right_servo.value = None
    left_servo.value = None

def fast_chopping(time_needed): 
    curr_time = time.time() 
    end_time = curr_time + time_needed 
    while curr_time < end_time: 
        right_servo.value = convert_angle_to_servo_value(180) # TODO: figure out the value that it should move to here
        left_servo.value = convert_angle_to_servo_value(0)
        time.sleep(0.2)
        right_servo.value = convert_angle_to_servo_value(0)
        left_servo.value = convert_angle_to_servo_value(180)
        time.sleep(0.2)
        curr_time = time.time()
    right_servo.value = None
    left_servo.value = None