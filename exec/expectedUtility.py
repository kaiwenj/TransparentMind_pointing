class GetEEU(object):
    
    def __init__(self, pbvi):
        self.pbvi=pbvi
        
    def __call__(self, b, a):
        _, V=self.pbvi(b)
        VA=[alpha for alpha in V if alpha['action']==a]
        EEU=[sum([alpha['alpha'][s]*bs for s, bs in b.items()]) for alpha in VA]
        maxEEU=max(EEU)
        return maxEEU
    
class GetEU(object):
    
    def __init__(self, pbvi, argmaxAlpha):
        self.pbvi=pbvi
        self.argmaxAlpha=argmaxAlpha
        
    def __call__(self, b, a, s):
        _, V=self.pbvi(b)
        VA=[alpha for alpha in V if alpha['action']==a]
        optimalAlpha=self.argmaxAlpha(VA, b)
        EU=optimalAlpha['alpha'][s]
        return EU
