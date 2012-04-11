import scipy.linalg

class SINRModel:
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
        
        print 'interference:', interference

        for (s, r) in links:
            dist = scipy.linalg.norm(s - r)
            S = self.config.power / dist ** self.config.alpha
            local_interference = interference - S
            IN = local_interference + self.config.noise()
            
            print 'S:', S
            print 'dist:', dist
            print 'power:', self.config.power
            print 'alpha:', self.config.alpha
            print 'IN:', IN

            if IN > 0:
                sinr = S / IN
                print 'sinr:', sinr

                if sinr >= self.config.beta:
                    success.append((s, r))
                else:
                    failed.append((s, r))
            else:
                success.append((s, r))
                
        return success, failed
