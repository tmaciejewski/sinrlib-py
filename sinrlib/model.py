import scipy.linalg

class Link:
    def __init__(self, s, r):
        self.s = scipy.array(s)
        self.r = scipy.array(r)
        
    def __iter__(self):
        return iter((self.s, self.r))

class Model:
    def __init__(self, config):
        self.config = config

    def eval(self, links):
        interference = 0
        success = []
        failed = []

        for (s, r) in links:
            dist = scipy.linalg.norm(s - r)
            S = self.config.power / dist ** self.config.alpha
            interference += S
        
        for (s, r) in links:
            dist = scipy.linalg.norm(s - r)
            S = self.config.power / dist ** self.config.alpha
            local_interference = interference - S
            IN = local_interference + self.config.noise()

            if IN > 0:
                sinr = S / IN

                if sinr >= self.config.beta:
                    success.append((s, r))
                else:
                    failed.append((s, r))
            else:
                success.append((s, r))
                
        return success, failed
