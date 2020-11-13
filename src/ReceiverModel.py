class ReceiverModel(object):
    
    def __init__(self, getEEU, getProbMessageGivenState, actionSpace):
        self.getEEU=getEEU
        self.getProbMessageGivenState=getProbMessageGivenState
        self.actionSpace=actionSpace
        
    def __call__(self, b, m):
        unnormalizedBPrime={s: self.getProbMessageGivenState(m, s)*bs for s, bs in b.items()}
        normalizationConstantBPrime=sum(unnormalizedBPrime.values())
        bPrime={s: unnormalizedBs/normalizationConstantBPrime for s, unnormalizedBs in unnormalizedBPrime.items()}
        euOfAPrime={a: self.getEEU(bPrime, a) for a in self.actionSpace}
        aPrime=max(euOfAPrime, key=euOfAPrime.get)
        return bPrime, aPrime
