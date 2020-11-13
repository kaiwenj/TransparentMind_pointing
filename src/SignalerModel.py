import numpy as np

class SignalerModel(object):
    
    def __init__(self, getEU, getMCost, getABPrime, messageSpace):
        self.getEU=getEU
        self.getMCost=getMCost
        self.getABPrime=getABPrime
        self.messageSpace=messageSpace
        
    def __call__(self, b, s):
        receiverResponseGivenM={m: self.getABPrime(b, m) for m in self.messageSpace}
        vi={m: self.getEU(bPrime, aPrime, s)-self.getMCost(m) for m, (bPrime, aPrime) in receiverResponseGivenM.items()}
        unnormalizedProbMessage={m: np.exp(vim) for m, vim in vi.items()}
        normalizationConstantProbMessage=sum(unnormalizedProbMessage.values())
        probMGivenS={m: unnormalizedPmGivenS/normalizationConstantProbMessage for m, unnormalizedPmGivenS in unnormalizedProbMessage.items()}
        return probMGivenS
