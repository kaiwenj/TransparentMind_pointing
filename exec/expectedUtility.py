class GetEU(object):
    
    def __init__(self, pbviWithV, backupStartAction):
        self.pbviWithV=pbviWithV
        self.backupStartAction=backupStartAction
        
    def __call__(self, b, a, s):
        _, V=self.pbviWithV(b)
        beta=self.backupStartAction(V, b, a)
        eu=beta['alpha'][s]
        return eu
    
