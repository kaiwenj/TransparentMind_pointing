class ReceiverModel(object):
    
    def __init__(self, pomdpSolver, getProbMessageGivenState):
        self.pomdpSolver=pomdpSolver
        self.getProbMessageGivenState=getProbMessageGivenState
        
    def __call__(self, bRec, m):
        unnormalizedBRecPrime={s: self.getProbMessageGivenState(bRec, m, s)*bs for s, bs in bRec.items()}
        normalizationConstantBRecPrime=sum(unnormalizedBRecPrime.values())
        bRecPrime={s: unnormalizedBRecs/normalizationConstantBRecPrime for s, unnormalizedBRecs in unnormalizedBRecPrime.items()}
        aPrime=self.pomdpSolver(bRecPrime)
        return bRecPrime, aPrime
    
