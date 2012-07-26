class Algorithm:
    def init(self, nodes, links):
        return set()

    def on_round_end(self, uid, messages, round_number):
        return

    def is_done(self):
        return True

class AlgorithmFailed(Exception):
    pass

class Simulation:
    def __init__(self, model, noise_factory):
        self.model = model
        self.noise_factory = noise_factory

    def run(self, algorithm, max_rounds = 1000000):
        self.success = 0
        self.failed = 0
        self.empty_rounds = 0
        round_number = 0
        warn_step = int(max_rounds / 10)

        last_act = 0

        # setup noise
        for uid in self.model.nodes:
            self.model.nodes[uid].noise = self.noise_factory()

        # get the source from model
        source = self.model.source

        # init algorithm
        algorithm.init(self.model.nodes, self.model.links, source)

        senders = [source]

        while not algorithm.is_done():
            new_senders = []
            messages = {}

            if round_number % warn_step == 0 and round_number > 0:
                print 'round:', round_number
 
            if round_number > max_rounds:
                raise AlgorithmFailed


            if len(senders) == 0:
                self.empty_rounds += 1

            # eval model
            receivers = self.model.eval(senders)
            #print round_number, '| senders:', senders, 'receivers:', receivers

            for uid in self.model.nodes:
                if uid in receivers:
                    messages = receivers[uid]
                else:
                    messages = []

                if algorithm.on_round_end(uid, messages, round_number):
                    new_senders.append(uid)

            senders = new_senders

            round_number += 1

        return round_number
