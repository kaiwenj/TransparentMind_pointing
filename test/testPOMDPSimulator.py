import sys
sys.path.append('../src/')

import unittest
from ddt import ddt, data, unpack
import POMDPSimulator as targetCode

class TigerTransition():
    def __init__(self):
        self.transitionMatrix = {
            ('listen', 'tiger-left', 'tiger-left'): 1.0,
            ('listen', 'tiger-left', 'tiger-right'): 0.0,
            ('listen', 'tiger-right', 'tiger-left'): 0.0,
            ('listen', 'tiger-right', 'tiger-right'): 1.0,

            ('open-left', 'tiger-left', 'tiger-left'): 0.5,
            ('open-left', 'tiger-left', 'tiger-right'): 0.5,
            ('open-left', 'tiger-right', 'tiger-left'): 0.5,
            ('open-left', 'tiger-right', 'tiger-right'): 0.5,

            ('open-right', 'tiger-left', 'tiger-left'): 0.5,
            ('open-right', 'tiger-left', 'tiger-right'): 0.5,
            ('open-right', 'tiger-right', 'tiger-left'): 0.5,
            ('open-right', 'tiger-right', 'tiger-right'): 0.5
        }

    def __call__(self, state, action, nextState):
        nextStateProb = self.transitionMatrix.get((action, state, nextState), 0.0)
        return nextStateProb


class TigerReward():
    def __init__(self, rewardParam):
        self.rewardMatrix = {
            ('listen', 'tiger-left'): rewardParam['listen_cost'],
            ('listen', 'tiger-right'): rewardParam['listen_cost'],

            ('open-left', 'tiger-left'): rewardParam['open_incorrect_cost'],
            ('open-left', 'tiger-right'): rewardParam['open_correct_reward'],

            ('open-right', 'tiger-left'): rewardParam['open_correct_reward'],
            ('open-right', 'tiger-right'): rewardParam['open_incorrect_cost']
        }

    def __call__(self, state, action, sPrime):
        rewardFixed = self.rewardMatrix.get((action, state), 0.0)
        return rewardFixed


class TigerObservation():
    def __init__(self, observationParam):
        self.observationMatrix = {
            ('listen', 'tiger-left', 'tiger-left'): observationParam['obs_correct_prob'],
            ('listen', 'tiger-left', 'tiger-right'): observationParam['obs_incorrect_prob'],
            ('listen', 'tiger-right', 'tiger-left'): observationParam['obs_incorrect_prob'],
            ('listen', 'tiger-right', 'tiger-right'): observationParam['obs_correct_prob'],

            ('open-left', 'tiger-left', 'Nothing'): 1,
            ('open-left', 'tiger-right', 'Nothing'): 1,
            ('open-right', 'tiger-left', 'Nothing'): 1,
            ('open-right', 'tiger-right', 'Nothing'): 1,
        }

    def __call__(self, state, action, observation):
        observationProb = self.observationMatrix.get((action, state, observation), 0.0)
        return observationProb
    
@ddt
class TestPOMDPSimulator(unittest.TestCase):
        
    def assertNumericDictAlmostEqual(self, calculatedDictionary, expectedDictionary, places=7):
        self.assertEqual(calculatedDictionary.keys(), expectedDictionary.keys())
        for key in calculatedDictionary.keys():
            self.assertAlmostEqual(calculatedDictionary[key], expectedDictionary[key], places=places)
    
    def setUp(self):
        self.rewardParam={'listen_cost':-1, 'open_incorrect_cost':-100, 'open_correct_reward':10}
        self.rewardFunction=TigerReward(self.rewardParam)
        self.observationParam={'obs_correct_prob':0.85, 'obs_incorrect_prob':0.15}
        self.observationFunction=TigerObservation(self.observationParam)
        self.transitionFunction=TigerTransition()
        self.stateSpace=['tiger-left', 'tiger-right']
        self.observationSpace=['tiger-left', 'tiger-right', 'Nothing']
        self.actionSpace=['open-left', 'open-right', 'listen']
            
    @data(('tiger-left', 'open-right', 'Nothing', 10))
    @unpack
    def testOpenDoorCorrectReward(self, s, a, expectedO, expectedR):
        simulatePOMDP=targetCode.SimulatePOMDP(self.stateSpace, self.actionSpace, self.observationSpace, 
                                               self.transitionFunction, self.rewardFunction, self.observationFunction)
        _, calculatedR, calculatedO=simulatePOMDP(s, a)
        self.assertEqual(calculatedO, expectedO)
        self.assertAlmostEqual(calculatedR, expectedR)
        
    @data(('tiger-left', 'open-left', 'Nothing', -100))
    @unpack
    def testOpenDoorWrongReward(self, s, a, expectedO, expectedR):
        simulatePOMDP=targetCode.SimulatePOMDP(self.stateSpace, self.actionSpace, self.observationSpace, 
                                               self.transitionFunction, self.rewardFunction, self.observationFunction)
        _, calculatedR, calculatedO=simulatePOMDP(s, a)
        self.assertEqual(calculatedO, expectedO)
        self.assertAlmostEqual(calculatedR, expectedR)
        
    @data(('tiger-left', 'listen', 'tiger-left', 'Nothing', -1))
    @unpack
    def testListen(self, s, a, expectedS, excludedO, expectedR):
        simulatePOMDP=targetCode.SimulatePOMDP(self.stateSpace, self.actionSpace, self.observationSpace, 
                                               self.transitionFunction, self.rewardFunction, self.observationFunction)
        calculatedS, calculatedR, calculatedO=simulatePOMDP(s, a)
        self.assertEqual(calculatedS, expectedS)
        self.assertNotEqual(calculatedO, excludedO)
        self.assertAlmostEqual(calculatedR, expectedR)
        
    def tearDown(self):
        pass
 
if __name__ == '__main__':
	unittest.main(verbosity=2)
