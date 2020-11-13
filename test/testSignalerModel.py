import sys
sys.path.append('../src/')
import unittest
from ddt import ddt, data, unpack
import SignalerModel as targetCode


@ddt
class TestSignalerModel(unittest.TestCase):
        
    def assertNumericDictAlmostEqual(self, calculatedDictionary, expectedDictionary, places=7):
        self.assertEqual(calculatedDictionary.keys(), expectedDictionary.keys())
        for key in calculatedDictionary.keys():
            self.assertAlmostEqual(calculatedDictionary[key], expectedDictionary[key], places=places)
                  
    @data((lambda b, a, s: 1*(a==s), lambda m: 0, lambda b, m: (b, 1*(m==3)+1), [3, 5], {1:1/2, 2:1/2}, 1, {3:0.26894, 5:0.73106}))
    @unpack
    def testNotChangeBelief(self, getEU, getMCost, getABPrime, messageSpace, b, s, expectedResult):
        signalerModel=targetCode.SignalerModel(getEU, getMCost, getABPrime, messageSpace)
        calculatedResult=signalerModel(b, s)
        self.assertNumericDictAlmostEqual(calculatedResult, expectedResult, 5)
        
    @data((lambda b, a, s: max(b.values()), lambda m: 0, lambda b, m: ({1: m/10, 2: 1-m/10}, 1*(m==3)+1), [3, 5], {1:1/2, 2:1/2}, 1, 
           {3:0.54983, 5:0.45017}))
    @unpack
    def testChangeBelief(self, getEU, getMCost, getABPrime, messageSpace, b, s, expectedResult):
        signalerModel=targetCode.SignalerModel(getEU, getMCost, getABPrime, messageSpace)
        calculatedResult=signalerModel(b, s)
        self.assertNumericDictAlmostEqual(calculatedResult, expectedResult, 5)
        
    @data((lambda b, a, s: max(b.values()), lambda m: 6-m, lambda b, m: ({1: m/10, 2: 1-m/10}, 1*(m==3)+1), [3, 5], {1:1/2, 2:1/2}, 1, 
           {3:0.14185, 5:0.85815}))
    @unpack
    def testMessageCost(self, getEU, getMCost, getABPrime, messageSpace, b, s, expectedResult):
        signalerModel=targetCode.SignalerModel(getEU, getMCost, getABPrime, messageSpace)
        calculatedResult=signalerModel(b, s)
        self.assertNumericDictAlmostEqual(calculatedResult, expectedResult, 5)
        
    
    def tearDown(self):
        pass
 
if __name__ == '__main__':
	unittest.main(verbosity=2)
