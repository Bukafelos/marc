#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import rospkg
import cv2
import matplotlib.pylab as plt
import rospy
import sys, os
import json, time, math
import argparse
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan, Image, Joy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from ackermann_msgs.msg import AckermannDriveStamped
import keras
from keras.models import model_from_json
from keras import backend as K
import tensorflow as tf
from cv_bridge import CvBridge, CvBridgeError
rospy.init_node('predict')
K.clear_session()
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5
K.set_session(tf.Session(config=config))

parser = argparse.ArgumentParser()
parser.add_argument('--speed', nargs='?', type=float, help='Speed of the car', default=0.5, const=0.5)
args = parser.parse_args()

class BaseClass(object):
    def __init__(self):
        self.bridge = CvBridge()
        self.out = None
        self.angle = None
        self.speed = args.speed
        self.rate = rospy.Rate(20)
        self.index = 0
        self.debug = False
        self.image = None
        self.cropped_pixel_from_top = 100
        self.graph_behavioral = tf.get_default_graph()
        rospack = rospkg.RosPack()
        self.model_name = os.environ['HOME'] + '/marc_models/model_new'
        self.model = self.nn_model()
        rospy.Subscriber('/zed/zed_node/right/image_rect_color', Image, self.zed_callback, queue_size=1)
        self.pub = rospy.Publisher('/ackermann_cmd_mux/input/navigation', AckermannDriveStamped, queue_size=1)

    def get_img(self, img):
        img = cv2.resize(img, (320, 180))
        img = img[self.cropped_pixel_from_top:,:,:]
        img = img.reshape(1, 80, 320, 3)
        return img

    def zed_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        if self.debug:
            cv2.imshow('Image', self.image)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                pass

    def pipeline(self):

        with self.graph_behavioral.as_default():
            msg = AckermannDriveStamped()
            if not self.image is None:
                cv2_img = self.get_img(self.image)
                self.out = self.model.predict(cv2_img, batch_size=1)
                self.angle = self.out[0][0]
            else:
                self.angle = 0.0
            msg.drive.steering_angle = self.angle
            msg.drive.speed = self.speed
            rospy.loginfo('Predicted angle:' + str(self.angle))
            self.pub.publish(msg)
   
        self.rate.sleep()

    def nn_model(self):
        jstr = json.loads(open(self.model_name + '.json').read())
        model = model_from_json(jstr)
        model.load_weights(self.model_name + '.h5')
        return model
        
drive = BaseClass()
        
if __name__ == '__main__':
    while not rospy.is_shutdown():
    	drive.pipeline()
    rospy.spin()

