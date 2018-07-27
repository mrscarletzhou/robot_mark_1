#!/usr/bin/env python
# license removed for brevity
import rospy
import os , sys, select, termios, tty
import math
import curses
#import Tkinter as tk
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from math import pi

pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
my_msg = JointState()
screen = curses.initscr()
	
def mypublisher():


    rospy.init_node('publisher_2', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    my_msg.name=['base_to_left_front_wheel','base_to_left_back_wheel','base_to_right_front_wheel','base_to_right_back_wheel', 'base_to_right_arm_1', 'base_to_left_arm_1', 'joint_of_left_arm', 'joint_of_right_arm']
    my_msg.position = [0,0,0,0,0,0,0,0]
    i=0#the position of all four wheels
    jr1=0#position of base_to_right_arm_1
    jr2=0#position of joint_of_right_arm
    jl1=0#position of base_to_left_arm_1
    jl2=0#position of joint_of_left_arm
    i_1=0
    while not rospy.is_shutdown():

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        old_settings[3] = old_settings[3] & ~termios.ICANON & ~termios.ECHO
        try :
            tty.setraw( fd )
            ch = sys.stdin.read( 1 )
	    curses.noecho()
            curses.curs_set(0)
	    event = screen.getch()
        finally :
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
 
        my_msg.header.seq = i_1
        my_msg.header.stamp = rospy.Time.now() 
  	#my_msg.position = [i*0.0314,0,0,0,0,0,0,0]
        ##my_msg.velocity = [i,i,i,i,i,i,i,i]
	if event == curses.KEY_LEFT:
                i=i+1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 's':
		i=i-1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'k':
		jr1=jr1+1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'l':
		jr1=jr1-1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]	
	elif ch == 'h':
		jl1=jl1+1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'j':
		jl1=jl1-1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'y':
		jl2=jl2+1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'u':
		jl2=jl2-1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'o':
		jr2=jr2+1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'p':
		jr2=jr2-1
		my_msg.position = [i*pi/2,i*pi/2,i*pi/2,i*pi/2,jr1*pi/20,jl1*pi/20,jl2*pi/20,jr2*pi/20]
	elif ch == 'q':
		exit()
 
        i_1 = i_1 + 1
	rospy.loginfo(my_msg)
        pub.publish(my_msg)
        

        rate.sleep()

	stop_robot();

def stop_robot():
    #cmd.linear.x = 0.0
   # cmd.angular.z = 0.0
    pub.publish(my_msg)


if __name__ == '__main__':
    try:
        mypublisher()
    except rospy.ROSInterruptException:
        pass
