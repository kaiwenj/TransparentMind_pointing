import sys
sys.path.append('../../PBVI/src')
sys.path.append('../exec')

import unittest
from ddt import ddt, data, unpack
import expectedUtility as targetCode

from PBVI import argmaxAlpha

@ddt
class TestGetEEU(unittest.TestCase):

    
    def setUp(self):
        self.pbvi=lambda b: ({'action': 1, 'alpha':{1: 2, 3: 4, 5: 6}},
                             [{'action': 1, 'alpha':{1: 2, 3: 4, 5: 6}},
                              {'action': 1, 'alpha':{1: -2, 3: -4, 5: 6}},
                              {'action': 2, 'alpha':{1: -2, 3: 4, 5: -6}},
                              {'action': 2, 'alpha':{1: 2, 3: -4, 5: 6}}])
        
    @data(({1: 1/2, 3: 1/4, 5: 1/4}, 1, 3.5))
    @unpack
    def testOptimalAction(self, b, a, expectedResult):
        getEEU=targetCode.GetEEU(self.pbvi)
        calculatedResult=getEEU(b, a)
        self.assertAlmostEqual(calculatedResult, expectedResult)
        
    @data(({1: 1/2, 3: 1/4, 5: 1/4}, 2, 1.5))
    @unpack
    def testSubOptimalAction(self, b, a, expectedResult):
        getEEU=targetCode.GetEEU(self.pbvi)
        calculatedResult=getEEU(b, a)
        self.assertAlmostEqual(calculatedResult, expectedResult)
        
        
    def tearDown(self):
        pass

@ddt
class TestGetEU(unittest.TestCase):

    
    def setUp(self):
        self.pbvi=lambda b: ({'action': 1, 'alpha':{1: 2, 3: 4, 5: 6}},
                             [{'action': 1, 'alpha':{1: 2, 3: 4, 5: 6}},
                              {'action': 1, 'alpha':{1: -2, 3: -4, 5: 6}},
                              {'action': 2, 'alpha':{1: -2, 3: 4, 5: -6}},
                              {'action': 2, 'alpha':{1: 2, 3: -4, 5: 6}}])
        self.argmaxAlpha=argmaxAlpha
        
    @data(({1: 1/2, 3: 1/4, 5: 1/4}, 1, 5, 6))
    @unpack
    def testOptimalAction(self, b, a, s, expectedResult):
        getEU=targetCode.GetEU(self.pbvi, self.argmaxAlpha)
        calculatedResult=getEU(b, a, s)
        self.assertAlmostEqual(calculatedResult, expectedResult)
        
    @data(({1: 1/2, 3: 1/4, 5: 1/4}, 2, 3, -4))
    @unpack
    def testSubOptimalAction(self, b, a, s, expectedResult):
        getEU=targetCode.GetEU(self.pbvi, self.argmaxAlpha)
        calculatedResult=getEU(b, a, s)
        self.assertAlmostEqual(calculatedResult, expectedResult)
        
        
    def tearDown(self):
        pass



if __name__ == '__main__':
	unittest.main(verbosity=2)
