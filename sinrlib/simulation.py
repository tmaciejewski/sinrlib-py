import model

class Simulation:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def run(self, rounds, config, initial_state):
        m = model.Model(config)
        links = initial_state

        print 'Starting', rounds, 'rounds with initial state:', \
            initial_state

        for i in range(rounds):
            sent, failed = m.eval(links)
            new_links = []

            print 'round:', i
            print 'sent:', sent
            print 'failed:', failed

            for _, r in sent:
                try:
                    new_s = self.algorithm(r, True)
                    if new_s != None:
                        new_links.append(model.Link(r, new_s))
                except Exception as e:
                    print 'The algorithm for', r, 'raised an exception'

            links = new_links

