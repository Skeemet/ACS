# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 09:14:58 2020

@author: Squall'ss

"""

import os
import configparser
import time
from shutil import copyfile
import cv2
import numpy as np

import sys
from pyzbar import pyzbar


##TODO : make a more robust barcode reader
#https://www.pyimagesearch.com/2014/11/24/detecting-barcodes-images-python-opencv/
# then implement configuration's determination from number -> see module
#number 13 digits
# first 9 -> unique_id_number
# 2 number for a letter
# 2 digits for configuration's number
# last digit is a control key

class Control:
    def __init__(self):
        #init source path
        # source_path is the path of the ACS folder
        # '/../' if __main__='__main__'
        #current_directory_path = os.getcwd()
        print(os.getcwd())
        print(os.getcwd().split('\\')[-1])
        if os.getcwd().split('\\')[-1] == 'ACS':
            self.source_path = ''
        elif os.getcwd().split('\\')[-1] == 'source':
            self.source_path = '../'
        else:
            print("Environment not resolved. Your environment is :")
            print(os.getcwd())

        #self.source_path = source_path
        #self.temp_directory_path = self.source_path + 'actuators/temp/'
        
        
    def run(self):
        """Perform control of one actuator"""
        print("it's running dude")
        self.take_photo()
        self.determine_configuration()
        self.prepare_analysis()
        self.determine_tests_to_do()
        self.run_tests()
        self.make_judgment()

    def test_path(self):
        print()
        
        
    def take_photo(self):
        """Take photo of an actuator.
        For this it interracts with raspberry pi and UR10.
        """
        
        #implementation with rpi pins and ur10
        #...
        
        #temp directory path
        file_name = 'test.txt'
        file_directory_path = self.source_path + 'actuators/temp' + file_name
        
#        #here the file is created only for testing the path
#        f = open(file_directory_path, 'w')
#        f.write('test of the path\n')
#        f.write(file_directory_path)
#        f.close()
        
        #save them in temp directory
        #...
        
        #set their name as attibuts of Control class to use them later
        self.picture_name = ['picture_'+letter+'.jpg' for letter in ['a', 'b', 'c', 'd', 'e']]
        
        #create fake pictures which simulate process of taking photo
        print(os.getcwd())
        print(self.source_path)
        for picture in self.picture_name:
            copyfile(self.source_path+'config/photo_not_taken/'+picture, self.source_path+'actuators/temp/'+picture)
        
        return self.picture_name
        
    def determine_configuration(self):
        """Read QR code on view_e
        extract actuator's MAC number and acuator's configuration
        return a string : actuator's configuration"""
        
        #read QR code on view_e.jpg
#        image = cv2.imread('ean13_1478964523487.png') #code0.png
        image = cv2.imread(self.source_path+'actuators/temp/picture_e.jpg')
        # find the barcodes in the image and decode each of the barcodes
        barcodes = pyzbar.decode(image)
        
        # loop over the detected barcodes
        for barcode in barcodes:
        	# extract the bounding box location of the barcode and draw the
        	# bounding box surrounding the barcode on the image
        	(x, y, w, h) = barcode.rect
        	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
        	# the barcode data is a bytes object so if we want to draw it on
        	# our output image we need to convert it to a string first
        	barcodeData = barcode.data.decode("utf-8")
        	barcodeType = barcode.type
            
        	# draw the barcode data and barcode type on the image
        	text = "{} ({})".format(barcodeData, barcodeType)
        	cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
        		0.5, (0, 0, 255), 2)
            
        	# print the barcode type and data to the terminal
        	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
            
        # show the output image
        #cv2.imshow("Image", image)
        #cv2.waitKey(0)
        cv2.imwrite(self.source_path+"actuators/temp/barcode_analysis.jpg", image)

        #analys and extract actuator's MAC number and acuator's configuration
        # TODO: modify self.actuator_configuration_expected par la valeur que l'on lit dans le QR code
        self.actuator_configuration_expected = "D0"
    
    
    def prepare_analysis(self):
        """make sure to close self.report object after using this method
        
        make a method to create all folders
        one for moving files
        one for init config files"""
        
        #determine actuator number
        config_directory = self.source_path+'config/'
        config_filname = 'global_parameter.cfg'
        config = configparser.ConfigParser()
        config.read(config_directory+config_filname)
        
        ##if file (and section) not exist then create them
        if not 'Variable' in config:
            print('création of config file')
            actuator_number = 0
            config.add_section('Variable')
            config['Variable']['actuator_last_number'] = str(actuator_number)
            
            with open(self.source_path+"config/global_parameter.cfg", 'w') as config_file:
                config.write(config_file)
        
        ##read precedent value
        config = configparser.ConfigParser()
        config.read(self.source_path+"config/global_parameter.cfg")
        actuator_number = config.getint('Variable', 'actuator_last_number')
        actuator_number += 1
        print(actuator_number)
        
        #save actual actuator_number
        config['Variable']['actuator_last_number'] = str(actuator_number)
        with open(self.source_path+"config/global_parameter.cfg", 'w') as config_file:
            config.write(config_file)
        
        #create actuator directory
        self.directory_name = 'actuators_' + str(actuator_number) +'_'+ self.actuator_configuration_expected
        
        if not os.path.exists(self.source_path+"actuators/" + self.directory_name):
            os.mkdir(self.source_path+"actuators/" + self.directory_name)
        
        #create picture directory
        if not os.path.exists(self.source_path+"actuators/" + self.directory_name + '/source_photo/'):
            os.mkdir(self.source_path+"actuators/" + self.directory_name + '/source_photo/')
            
        #move picture from temp directory to picture directory
        for picture in self.picture_name:
            os.replace(self.source_path+'actuators/temp/' + picture, self.source_path+'actuators/' + self.directory_name + '/source_photo/' + picture)
            
        #create directory find_photo
        if not os.path.exists(self.source_path+'actuators/' + self.directory_name + '/find_photo/'):
            os.mkdir(self.source_path+'actuators/' + self.directory_name + '/find_photo/')
        
        #move bacode analysis
        os.replace(self.source_path+"actuators/temp/barcode_analysis.jpg", self.source_path+"actuators/" + self.directory_name + "/find_photo/barcode_analysis.jpg")
        
        report_directory = self.source_path+'actuators/' + self.directory_name + '/report/'
        if not os.path.exists(report_directory):
            os.mkdir(report_directory)
        report_name = 'result_test.txt'
        self.report = report_directory + report_name
        
        #create report'headers
        report_name = 'details.txt'
        details = configparser.ConfigParser()
        headers_section = 'Headers'
        details.add_section(headers_section)
        details[headers_section]['date'] = str(time.time())
        details[headers_section]['actuator_number'] = str(actuator_number)
        
        #save headers
        with open(report_directory+report_name, 'w') as details_file:
            details.write(details_file)
        
        
    def determine_tests_to_do(self):
        
        config_directory = self.source_path+'config/'
        config_filname = 'actuator_config.cfg'
        config = configparser.ConfigParser()
        config.read(config_directory+config_filname)
        
        l_test = config[self.actuator_configuration_expected]['test_to_do']
        l_test = str(l_test).split(', ')
        print("tests list ", l_test, type(l_test))
        self.l_test = l_test
        
    def run_tests(self):
        l_result =  [] #list of booleen result
        for test_name in self.l_test:
            print("test name ", test_name)
            test = Test(
                    test_name,
                    self.actuator_configuration_expected, 
                    self.directory_name,
                    self.report)
            l_result.append(test.run())
        self.l_result = l_result
            
    def is_actuator_ok(self):
        l = self.l_result
        result = True
        for elem in l:
            result = result and elem
            if elem == False:
                return False
        return True
        
    def make_judgment(self):
        
        #get if actuator ok
        is_actuator_ok = self.is_actuator_ok()
        
        #write report
        report = configparser.ConfigParser()
        report.read(self.source_path+"actuators/" + self.directory_name + "/report/details.txt")
        report['Headers']['is_actuator_ok'] = str(True)
        with open(self.source_path+"actuators/" + self.directory_name + "/report/details.txt", 'w') as config_file:
            report.write(config_file)
        
        # TODO: write advanced report
        #print result acuator not good
        if is_actuator_ok:
            print("[BON] Le vérin a réussi le contrôle")
        else:
            print("[MAUVAIS] Le vérin présente des défauts, pour plus de dtails lire le rapport détaillé se situant ../acuators/"+self.directory_name+'/report')
        
        
class Test():
    
    def __init__(self, test_name, expected_configuration, directory_name, report):
        """e.g.
        expected_configuration -> 'D0'
        source_path -> ACS/
        actuator_path -> ACS/actuators/actuator_1294_D0/
        report -> report object (file) to write in result of test
        """
        self.directory_name = directory_name
        self.test_name = test_name
        self.report = report

        if os.getcwd().split('\\')[-1] == 'ACS':
            self.source_path = ''
        elif os.getcwd().split('\\')[-1] == 'source':
            self.source_path = '../'
        else:
            print("Environment not resolved. Your environment is :")
            print(os.getcwd())
        
        #open config file
        config_directory = self.source_path+'config/'
        config_filname = 'tests.cfg'
        config = configparser.ConfigParser()
        config.read(config_directory+config_filname)
        
        #extract from configfile important data for running a test
        self.template_name              = config[test_name]['template_name']
        self.picture_to_analyse         = config[test_name]['picture_to_analyse']
        self.threshold            = float(config[test_name]['threshold'])
        self.template_matching_strategy = config[test_name]['template_matching_strategy']
        self.methode_to_use             = config[test_name]['method_to_use']
        
        self.template_path           = self.source_path+'config/templates/' + self.template_name
        self.picture_to_analyse_path = self.source_path+'actuators/' + directory_name + '/source_photo/picture_' + self.picture_to_analyse + '.jpg'
        self.picture_to_save_name    = test_name + '_picture_' + self.picture_to_analyse + '.jpg'
        self.save_picture_directory  = self.source_path+'actuators/' + directory_name + '/find_photo/'
        self.save_picture_path       = self.save_picture_directory + self.picture_to_save_name
        
        #create directory to save photo
        if not os.path.exists(self.save_picture_directory):
            os.mkdir(self.save_picture_directory)
        
        print("\n Attributs of ", self)
        print(vars(self))
    
    def run(self):
        print("\nTest is running")
        
        #run method requeste by the test in config file
        return getattr(self, self.methode_to_use)()
        
    def standard_test(self):
        
        #to describe metrix
        # https://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
        
        print("\n[STANDARD_TEST]")
        img_rgb = cv2.imread(self.source_path+"actuators/" + self.directory_name + '/source_photo/picture_' + self.picture_to_analyse + '.jpg')
        
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(self.template_path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        
        res = cv2.matchTemplate(img_gray.astype(np.uint8),template.astype(np.uint8),cv2.TM_CCOEFF_NORMED)
        threshold = self.threshold
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    
        cv2.imwrite(self.source_path+"actuators/" + self.directory_name + '/find_photo/' + self.test_name +'_' + self.picture_to_analyse + '.jpg', img_rgb)
        
        #todo: analyse situation and create message
        self.write_report(True, "Success")
        return True
    
    def write_report(self, is_success, message):
        
        print("\nWriting report")
        if is_success == True:
            indicator = "[v];"
        else:
            indicator = "[x];"
        
        line = indicator + '<' + self.test_name + '>;' + message
        print(self.report)
        with open(self.report, 'a') as file:
            file.write(line)

        
if __name__ == "__main__":
    control = Control()
    control.run()
