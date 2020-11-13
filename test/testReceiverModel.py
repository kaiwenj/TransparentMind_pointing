import sys
sys.path.append('../src/')
import unittest
from ddt import ddt, data, unpack
import ReceiverModel as targetCode #change to file name


@ddt
class TestReceiverModel(unittest.TestCase):
        
    def assertNumericDictAlmostEqual(self, calculatedDictionary, expectedDictionary, places=7):
        self.assertEqual(calculatedDictionary.keys(), expectedDictionary.keys())
        for key in calculatedDictionary.keys():
            self.assertAlmostEqual(calculatedDictionary[key], expectedDictionary[key], places=places)
                  
    @data((lambda b, a: a, lambda m, s: 1*(m==s), [3, 5], {1:1/2, 2:1/2}, 1, ({1:1, 2:0}, 5)))
    @unpack
    def testTellingState(self, getEEU, getProbMessageGivenState, actionSpace, b, m, expectedResult):
        receiverModel=targetCode.ReceiverModel(getEEU, getProbMessageGivenState, actionSpace)
        calculatedResult=receiverModel(b, m)
        self.assertNumericDictAlmostEqual(calculatedResult[0], expectedResult[0])
        self.assertAlmostEqual(calculatedResult[1], expectedResult[1])
        
    @data((lambda b, a: a, lambda m, s: 0.8*(m==s)+0.2*(m!=s), [3, 5], {1:1/2, 2:1/2}, 1, ({1:0.8, 2:0.2}, 5)))
    @unpack
    def testTellingStateWithNoise(self, getEEU, getProbMessageGivenState, actionSpace, b, m, expectedResult):
        receiverModel=targetCode.ReceiverModel(getEEU, getProbMessageGivenState, actionSpace)
        calculatedResult=receiverModel(b, m)
        self.assertNumericDictAlmostEqual(calculatedResult[0], expectedResult[0])
        self.assertAlmostEqual(calculatedResult[1], expectedResult[1])
        
    @data((lambda b, a: a, lambda m, s: 0.8*(m==s)+0.2*(m!=s), [3, 5], {1:0.2, 2:0.8}, 1, ({1:0.5, 2:0.5}, 5)))
    @unpack
    def testNoisedMessageWithUnflatPrior(self, getEEU, getProbMessageGivenState, actionSpace, b, m, expectedResult):
        receiverModel=targetCode.ReceiverModel(getEEU, getProbMessageGivenState, actionSpace)
        calculatedResult=receiverModel(b, m)
        self.assertDictEqual(calculatedResult[0], expectedResult[0])
        self.assertAlmostEqual(calculatedResult[1], expectedResult[1])
        
    @data((lambda b, a: a, lambda m, s: 0.5, [3, 5], {1:0.2, 2:0.8}, 1, ({1:0.2, 2:0.8}, 5)))
    @unpack
    def testTellingStateWithRandomSignal(self, getEEU, getProbMessageGivenState, actionSpace, b, m, expectedResult):
        receiverModel=targetCode.ReceiverModel(getEEU, getProbMessageGivenState, actionSpace)
        calculatedResult=receiverModel(b, m)
        self.assertNumericDictAlmostEqual(calculatedResult[0], expectedResult[0])
        self.assertAlmostEqual(calculatedResult[1], expectedResult[1])
        
    @data((lambda b, a: a, lambda m, s: 0.9*(s==1)*(m==6)+0.1*(s==1)*(m==4)+0.4*(s==2)*(m==6)+0.6*(s==2)*(m==4), 
           [3, 5], {1:0.2, 2:0.8}, 4, ({1:0.04, 2:0.96}, 5)))
    @unpack
    def testMessageGeneralCase(self, getEEU, getProbMessageGivenState, actionSpace, b, m, expectedResult):
        receiverModel=targetCode.ReceiverModel(getEEU, getProbMessageGivenState, actionSpace)
        calculatedResult=receiverModel(b, m)
        self.assertNumericDictAlmostEqual(calculatedResult[0], expectedResult[0])
        self.assertAlmostEqual(calculatedResult[1], expectedResult[1])
        
    @data((lambda b, a: a*b[1]-0.5*a*b[2], lambda m, s: 0.9*(s==1)*(m==6)+0.1*(s==1)*(m==4)+0.4*(s==2)*(m==6)+0.6*(s==2)*(m==4), 
           [3, 5], {1:0.2, 2:0.8}, 4, ({1:0.04, 2:0.96}, 3)))
    @unpack
    def testUtility(self, getEEU, getProbMessageGivenState, actionSpace, b, m, expectedResult):
        receiverModel=targetCode.ReceiverModel(getEEU, getProbMessageGivenState, actionSpace)
        calculatedResult=receiverModel(b, m)
        self.assertNumericDictAlmostEqual(calculatedResult[0], expectedResult[0])
        self.assertAlmostEqual(calculatedResult[1], expectedResult[1])
    
    def tearDown(self):
        pass
        
if __name__ == '__main__':
	unittest.main(verbosity=2)
