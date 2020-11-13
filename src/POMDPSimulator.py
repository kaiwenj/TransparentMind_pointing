import numpy as np

class SimulatePOMDP(object):
    
    def __init__(self, stateSpace, actionSpace, observationSpace, transitionFunction, rewardFunction, observationFunction):
        self.stateSpace=stateSpace
        self.actionSpace=actionSpace
        self.observationSpace=observationSpace
        self.transitionFunction=transitionFunction
        self.rewardFunction=rewardFunction
        self.observationFunction=observationFunction
    
    def __call__(self, s, a):
        sPrimeDistribution={sPrime: self.transitionFunction(s, a, sPrime) for sPrime in self.stateSpace}
        sPrime=np.random.choice(list(sPrimeDistribution.keys()), p=list(sPrimeDistribution.values()))
        r=self.rewardFunction(s, a, sPrime)
        oDistribution={o: self.observationFunction(sPrime, a, o) for o in self.observationSpace}
        o=np.random.choice(list(oDistribution.keys()), p=list(oDistribution.values()))
        return (sPrime, r, o)
