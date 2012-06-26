class Algorithm:
    def init(self, nodes, links):
        return set()

    def on_round_end(self, uid, messages, round_number):
        return

    def is_done(self):
        return True

class Message:
    pass

class AlgorithmFailed(Exception):
    pass

class Simulation:
    def __init__(self, model, noise_factory):
        self.model = model
        self.noise_factory = noise_factory
        self.success = 0
        self.failed = 0
        self.empty_rounds = 0

    def run(self, algorithm):
        round_number = 0

        # setup noise
        for uid in self.model.nodes:
            self.model.nodes[uid].noise = self.noise_factory()

        # init algorithm
        senders = algorithm.init(self.model.nodes, self.model.links)

        while not algorithm.is_done():
            new_senders = set()
            messages = {}

            if round_number % 100000 == 0 and round_number > 0:
                print 'round:', round_number
 
            if round_number > 1000000:
                raise AlgorithmFailed


            if len(senders) == 0:
                self.empty_rounds += 1

            # eval model
            receivers = self.model.eval(senders)
            #print 'senders:', len(senders), 'receiver:', len(receivers)

            for uid in self.model.nodes:
                if uid in receivers:
                    messages[uid] = True
                else:
                    messages[uid] = False

                if algorithm.on_round_end(uid, messages[uid], round_number):
                    new_senders.add(uid)

            senders = new_senders

            round_number += 1

        return round_number
