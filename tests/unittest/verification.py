# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:32:16 2020

@author: Squall'ss
"""

import unittest
#import ../source/actuator_checker

import os

import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('../../source/')
sys.path.append('../source/')
sys.path.append('../../')


from actuator_checker import Control

print(Control)
#from testutils import RunTests
#from mock import Mock, sentinel, patch



class TestControl(unittest.TestCase):

    def setUp(self):
        source_path = os.getcwd() + '/../../'
        print(source_path)
        self.control = Control()#source_path)
        
    def test_upper(self):
        print(os.getcwd())
        self.assertEqual(self.control.take_photo(), ['picture_a.jpg',
 'picture_b.jpg',
 'picture_c.jpg',
 'picture_d.jpg',
 'picture_e.jpg'])

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()