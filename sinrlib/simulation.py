class Algorithm:
    def init(self, nodes, links):
        return set()

    def on_received(self, uid, message, sender):
        return

    def on_round_end(self, uid, round_number):
        return

    def is_done(self):
        return True

class Message:
    pass

class NotLinked(Exception):
    pass

class Simulation:
    def __init__(self, model):
        self.model = model

    def run(self, algorithm):
        senders = algorithm.init(self.model.nodes, self.model.links)
        round_number = 0

        while not algorithm.is_done():
            receivers = self.model.eval(senders)
            new_senders = set()
            for uid in receivers:
                if algorithm.on_received(uid, Message(), None):
                    new_senders.add(uid)

            for uid in self.model.nodes:
                if algorithm.on_round_end(uid, round_number):
                    new_senders.add(uid)

            senders = new_senders

            round_number += 1

            if round_number > 1000:
                return -1

        return round_number
