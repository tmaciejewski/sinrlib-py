import model

class Simulation:
    def __init__(self, _model):
        self.model = _model

    def run(self, rounds, algorithm, initial_state):
        links = initial_state

        print 'Starting', rounds, 'rounds with initial state:', \
            initial_state

        for i in range(rounds):
            sent, failed = self.model.eval(links)
            new_links = []

            print 'round:', i
            print 'sent:', sent
            print 'failed:', failed

            for s, r in sent:
                try:
                    new_s = algorithm(r, True, s, self.model.links[r])
                    if new_s != None:
                        new_links.append((r, new_s))
                except Exception as e:
                    print 'The algorithm for', r, 'raised an exception:', e.message

            links = new_links

