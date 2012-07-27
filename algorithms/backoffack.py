import random, math

class State:
    def __init__(self):
        self.broadcasting = False
        self.waiting_for_ack = False
        self.counter = 1
        self.counter_max = 1
        self.density = None
        self.ack_from = set()

class BackoffAckAlgorithm():
    def __init__(self, config):
        self.last_progress = 0

    def init(self, nodes, links, source):
        self.nodes = nodes
        self.N = len(nodes)
        self.active = set([source])
        self.state = {}
        for uid in self.nodes:
            self.state[uid] = State()
            neighbours = [u for u in self.nodes if u != uid \
                    and self.nodes[u] - self.nodes[uid] <= 1]
            self.state[uid].density = len(neighbours)
        self.state[source].broadcasting = True

    def on_round_end(self, uid, messages, round_number):
        state = self.state[uid]
        if state.broadcasting and round_number % 2 == 0:
            if state.counter > 0:
                state.counter -= 1
                if state.waiting_for_ack:
                    return self.waiting_for_ack(uid, messages, round_number)
                else:
                    return self.broadcast(uid, messages, round_number)
            else:
                # switched off
                return False
        elif not state.broadcasting and round_number % 2 == 1:
            return self.send_ack(uid, messages, round_number)
        else:
            return False

    def broadcast(self, uid, messages, round_number):
        state = self.state[uid]
        if state.counter == 0:
            # sending and waiting for ack
            #print uid, 'broadcasts and waits for ack for', state.counter_max, 'rounds'
            state.waiting_for_ack = True
            state.counter = state.counter_max + 1
            return True
        else:
            return False

    def waiting_for_ack(self, uid, messages, round_number):
        state = self.state[uid]
        acks = [s for s in messages if s not in state.ack_from]
        if acks != []:
            # got ack so start all over again
            #print uid, 'got acks:', acks
            state.ack_from.update(acks)
            state.counter = 1
            state.counter_max = 1
            state.waiting_for_ack = False
        elif state.counter == 0:
            # no ack
            #print uid, 'didn\'t get ack for last', state.counter_max, 'rounds'
            state.counter_max *= 2
            if state.counter_max > 2 * state.density:
                # no more acks
                #print uid, 'switching off'
                state.counter = -1
            else:
                #print uid, 'returns to broadcast'
                state.waiting_for_ack = False
                state.counter = random.randint(1, state.counter_max)
        return False

    def send_ack(self, uid, messages, round_number):
        state = self.state[uid]
        senders = [s for s in messages if self.state[s].broadcasting]
        if senders != []:
            # wakes up
            sender = senders[0]
            #print uid, 'woken up by', sender
            self.active.add(uid)
            state.counter_max = self.state[sender].counter_max
            state.counter = random.randint(1, state.counter_max)

        if uid in self.active:
            state.counter -= 1
            if state.counter == 0:
                #print uid, 'sends ack'
                state.broadcasting = True
                state.counter_max = 1
                state.counter = 1
                return True
        else:
            # still sleeping
            return False


    def is_done(self):
        progress = len(self.active) / float(self.N)
        if progress > self.last_progress:
            self.last_progress = progress
            #print 'progress:', progress
        return len(self.active) == self.N

