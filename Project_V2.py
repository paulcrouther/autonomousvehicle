# -*- coding: utf-8 -*-
import smbus
import time
import random
import math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)


# This is the address we setup in the Arduino Program
address_1 = 0x04#Slave

# Initialize values
agent_dir = 1;
agent_movement = 10.0
old_loc_x = 100.0
old_loc_y = 100.0
update_loc_x = 0
update_loc_y = 0
distance_betw_agent_dest = 0;
root_2 = 1.414
update_agent_dir = 1;
old_agent_dir = 1;
degree_agent_destination = 0
ultra_distance = 0.0
flag_stop = 0


print "Distance Measurement in Progress"
#TRIG = 23
#ECHO = 24
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.IN)

GPIO.output(23,False)
print "Waiting For Sensor to Settle"
time.sleep(0.5)

def writeNumber_1(value):
    bus.write_byte(address_1, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber_1():
    number = bus.read_byte(address_1)
    # number = bus.read_byte_data(address, 1)
    return number

def update_agent_location(agent_loc_x, agent_loc_y, var, agent_dir):
    #Algorithm for location_X, location_Y
    if (agent_dir == 1):#D1
        if(var == 2):
            new_loc_x = agent_loc_x - root_2*agent_movement
            new_loc_y = agent_loc_y - root_2*agent_movement
        elif (var == 3):
            new_loc_x = agent_loc_x + root_2*agent_movement
            new_loc_y = agent_loc_y - root_2*agent_movement
        else:
            new_loc_x = agent_loc_x
            new_loc_y = agent_loc_y - agent_movement
    elif(agent_dir == 2):#D2
        if(var == 2):
            new_loc_x = agent_loc_x - agent_movement
            new_loc_y = agent_loc_y
        elif (var == 3):
            new_loc_x = agent_loc_x
            new_loc_y = agent_loc_y - agent_movement
        else:
            new_loc_x = agent_loc_x - root_2*agent_movement
            new_loc_y = agent_loc_y - root_2*agent_movement
    elif(agent_dir == 3):#D3
        if(var == 2):
            new_loc_x = agent_loc_x - root_2*agent_movement
            new_loc_y = agent_loc_y + root_2*agent_movement
        elif(var ==3):
            new_loc_x = agent_loc_x - root_2*agent_movement
            new_loc_y = agent_loc_y - root_2*agent_movement
        else:
            new_loc_x = agent_loc_x - agent_movement
            new_loc_y = agent_loc_y
    elif(agent_dir == 4):#D4
        if(var == 2):
            new_loc_x = agent_loc_x
            new_loc_y = agent_loc_y + agent_movement
        elif(var ==3):
            new_loc_x = agent_loc_x - agent_movement
            new_loc_y = agent_loc_y
        else:
            new_loc_x = agent_loc_x - root_2*agent_movement
            new_loc_y = agent_loc_y + root_2*agent_movement
    elif(agent_dir == 5):#D5
        if(var == 2):
            new_loc_x = agent_loc_x + root_2*agent_movement
            new_loc_y = agent_loc_y + root_2*agent_movement
        elif(var == 3) :
            new_loc_x = agent_loc_x - root_2*agent_movement
            new_loc_y = agent_loc_y + root_2*agent_movement
        else:
            new_loc_x = agent_loc_x
            new_loc_y = agent_loc_y + agent_movement
    elif(agent_dir == 6):#D6
        if(var == 2):
            new_loc_x = agent_loc_x + agent_movement
            new_loc_y = agent_loc_y
        elif(var == 3):
            new_loc_x = agent_loc_x
            new_loc_y = agent_loc_y + agent_movement
        else:
            new_loc_x = agent_loc_x + root_2*agent_movement
            new_loc_y = agent_loc_y + root_2*agent_movement
    elif(agent_dir == 7):#D7
        if(var == 2):
            new_loc_x = agent_loc_x + root_2*agent_movement
            new_loc_y = agent_loc_y - root_2*agent_movement
        elif(var == 3):
            new_loc_x = agent_loc_x + root_2*agent_movement
            new_loc_y = agent_loc_y + root_2*agent_movement
        else:
            new_loc_x = agent_loc_x + agent_movement
            new_loc_y = agent_loc_y
    elif(agent_dir == 8):#D8
        if(var == 2):
            new_loc_x = agent_loc_x
            new_loc_y = agent_loc_y - agent_movement
        elif(var == 3):
            new_loc_x = agent_loc_x + agent_movement
            new_loc_y = agent_loc_y
        else:
            new_loc_x = agent_loc_x + root_2*agent_movement
            new_loc_y = agent_loc_y - root_2*agent_movement
    else:
        print "Wrong direction data"
        new_loc_x = -1
        new_loc_y = -1
    return (new_loc_x, new_loc_y)

def update_agent_direction(agent_dir,var):
    if (var == 2):#Left
        new_agent_dir = agent_dir + 1
        if(new_agent_dir == 9):
            new_agent_dir = 1
    elif(var == 3):#Right
        new_agent_dir = agent_dir - 1
        if(new_agent_dir == 0):
            new_agent_dir = 8
    else:#Foward
        new_agent_dir = agent_dir
    return new_agent_dir

def calculate_degree(direction):
    deg = 0;
    if (direction == 1):
        deg = 0
    elif(direction == 2):
        deg = 45
    elif(direction == 3):
        deg = 90
    elif(direction == 4):
        deg = 135
    elif(direction == 5):
        deg = 180
    elif(direction == 6):
        deg = 225
    elif(direction == 7):
        deg = 270
    elif(direction == 8):
        deg = 315
    else:
        print "Wrong direction"
        deg = -1
    return deg

def calculate_degreen_betw_agnet_destination(loc_x, loc_y, dir_agent):
    theta = math.degrees(math.atan(loc_x/loc_y))
    temp_degree_betw_agent_dest = dir_agent - theta
    degree_betw_agent_dest = math.fabs(temp_degree_betw_agent_dest)
    if(degree_betw_agent_dest > 180):
        degree_betw_agent_dest = degree_betw_agent_dest - 180
    return degree_betw_agent_dest

def distance_ultra_betw_agent_obs(trig_pin,echo_pin):

    GPIO.output(trig_pin,True)
    time.sleep(0.00001)
    GPIO.output(trig_pin,False)

    while GPIO.input(echo_pin)==0:
        pulse_start=time.time()

    while GPIO.input(echo_pin)==1:
        pulse_end=time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance , 2)
    return distance

#Start Collect Data

while True:
    random_var = input("Start 1 – 3: ")
    if not random_var:
        continue
    writeNumber_1(random_var)
    time.sleep(2)
    number = readNumber_1()
    print "Arduino: Hey RPI, I received a digit ", number
    print
    if (number != 1):
        if (number == 2):
            print "The agent arrives at destination"
            print
        elif (number == 3):
            print "The agent Left collision"
            print
            writeNumber_1(4)
        elif (number == 4):
            print "The agent Right collision"
            print
            writeNumber_1(5)
        elif (number == 5):
            print "The agent Both collision"
            print
            writeNumber_1(6)
        else:
            print "Something is wrong!"
            print
            
    else:
        #Update agent location
#        update_loc_x, update_loc_y = update_agent_location(old_loc_x, old_loc_y, random_var, old_agent_dir)
        #Calculate Distance between the agent and destination
#        distance_betw_agent_dest = math.sqrt(update_loc_x*update_loc_x + update_loc_y*update_loc_y)
        #New agent Direction
#        update_agent_dir = update_agent_direction(old_agent_dir,random_var)
        #Calculate Degree
#        degree_agent_dir = calculate_degree(update_agent_dir)
#        degree_betw_agent_destnation = calculate_degreen_betw_agnet_destination(update_loc_x, update_loc_y, degree_agent_dir)
        #Get Ultrasonic distance
        ultra_distance = distance_ultra_betw_agent_obs(23,24)
#        print "New Location : ", update_loc_x, ", ", update_loc_y
#        print "Distance : ", distance_betw_agent_dest
#        print "Agent Direction : ", update_agent_dir
#        print "Degree : ", degree_betw_agent_destnation
        print "Ultrasonic Distance : ", ultra_distance, "cm"
#        old_loc_x = update_loc_x
#        old_loc_y = update_loc_y
#        old_agent_dir = update_agent_dir
        random_var = 0
    
