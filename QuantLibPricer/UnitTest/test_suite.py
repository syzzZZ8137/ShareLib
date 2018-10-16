# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 10:09:54 2018

@author: gxjy-003
"""

# -*- coding: utf-8 -*-

import unittest
import testOptionPricer

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testOptionPricer))

    #输出txt格式测试报告
    with open('UnittestTextReport.txt', 'a') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)

