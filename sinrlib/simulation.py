class Algorithm:
    def init(self, nodes, links):
        return set()

    def on_received(self, uid, message, sender):
        return

    def new_round(self, round_number):
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
        round = 0

        while not algorithm.is_done():
            receivers = self.model.eval(senders)
            for uid in receivers:
                if not algorithm.on_received(uid, Message(), None):
                    receivers.remove(uid)

            senders = receivers

            round += 1

            if round > 10:
                return -1

        return round
