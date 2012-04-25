import model

class Algorithm:
    def init(self, uid, links):
        return []

    def compute(self, uid, message, sender, links):
        return []

class Simulation:
    def __init__(self, _model):
        self.model = _model

    def run(self, rounds, algorithm):
        messages = []
        for node in self.model.nodes.keys():
            for receiver in algorithm.init(node, self.model.links[node]):
                messages.append((node, receiver))

        print 'Starting', rounds, 'rounds with initial state:', \
            messages

        for i in range(rounds):
            sent, failed = self.model.eval(messages)
            new_messages = []

            print 'round:', i
            print 'sent:', sent
            print 'failed:', failed

            for s, r in sent:
                try:
                    for receiver in algorithm.compute(r, True, s, self.model.links[r]):
                        new_messages.append((r, receiver))

                except Exception as e:
                    print 'The algorithm for', r, 'raised an exception:', e.message

            messages = new_messages

