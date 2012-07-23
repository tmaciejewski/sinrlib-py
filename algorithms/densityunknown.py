import random, math

class State:
    def __init__(self, x, y, gamma):
        self.leader = None
        box_x = int(x / gamma)
        box_y = int(y / gamma)
        self.box = (box_x, box_y)
        self.leaders_transimts = True
        self.phase_round = 0
        self.conflict = False
        self.known_leaders = set()

    def __str__(self):
        return '(leader = %s, box = %s, known_leaders = %s)' \
                % (self.leader, self.box, self.known_leaders)

class DensityUnknownAlgorithm():
    def __init__(self, config, e, C):
        self.alpha = config.alpha
        self.e = e
        self.C = C
        self.gamma = e / (math.sqrt(2) * 6)
        self.last_progress = 0

    def init(self, nodes, links):
        self.nodes = nodes
        self.N = len(nodes)
        self.d = 4
        self.logn = int(math.log(self.N))
        self.dprim = 4
        self.state = {}
        for uid in self.nodes:
            self.state[uid] = State(nodes[uid].x, nodes[uid].y, self.gamma)
        source = random.choice(self.nodes.keys())
        self.state[source].leader = source
        self.active = {source}
        return {}

    def on_round_end(self, uid, messages, round_number):
        state = self.state[uid]

        if messages != []:
            self.active.add(uid)

        if state.leaders_transimts:
            res = self.leaders_transmits(uid, messages, round_number)
            state.phase_round += 1
            if state.phase_round >= self.d**2:
                state.leaders_transimts = False
                state.phase_round = [0, 0, 0]
                state.conflict = False
        else:
            if state.conflict == False and state.leader == None:
                res = self.leader_election(uid, messages, round_number)
            elif state.leader == uid:
                # leader election helper
                res = self.election_helper(uid, messages, round_number)

            state.phase_round[2] += 1

            if state.phase_round[2] > 2:
                state.phase_round[2] = 0
                state.phase_round[1] += 1

            if state.phase_round[1] > self.logn:
                state.phase_round[1] = 0
                state.phase_round[0] += 1

            if state.phase_round[0] >= self.dprim**2:
                state.leaders_transimts = False
                state.phase = 0

        return res

    def leaders_transmits(self, uid, messages, round_number):
        state = self.state[uid]

        for sender in messages:
            state.known_leaders.add(sender)
            print uid, 'know a leader', sender

        if state.leader == uid:
            a = int(state.phase_round / self.d)
            b = int(state.phase_round % self.d)
            if state.box[0] % self.d == a and state.box[1] % self.d == b:
                #print uid, 'transmits'
                return True
            else:
                #print 'in', state.box, 'not transmiting because of', (a,b)
                return False

    def leader_election(self, uid, messages, round_number):
        state = self.state[uid]

        a = int(state.phase_round[0] / self.d)
        b = int(state.phase_round[0] % self.d)
        if state.box[0] % self.d == a and state.box[1] % self.d == b:
            if state.phase_round[2] == 0:
                pbb = (1 / self.N) * 2 ** state.phase_round[1]
                # transmit with pbb
            elif state.phase_round[2] == 1:
                # wait for u
                pass
            elif state.phase_round[2] == 2:
                # if heard u? if transmitted, I'm the leader
                # transmitting if leader
                pass
            elif state.phase_round[2] == 3:
                # other nodes receiver the leader's and u's message
                pass

    def election_helper(self, uid, messages, round_number):
        state = self.state[uid]
        if state.phase_round[2] == 0:
            # wait for leader candidate
            pass
        elif state.phase_round[2] == 1:
            # respond to the leader candidate
            pass
        elif state.phase_round[2] == 2:
            # transmit with the leader
            pass
        elif state.phase_round[2] == 3:
            # wait for other
            pass

    def is_done(self):
        progress = len(self.active) / float(self.N)
        if progress > self.last_progress:
            self.last_progress = progress
            print 'progress:', progress
        
        #return len(self.active) == self.N
        if len(self.active) > 1:
            for uid in self.nodes:
                print uid, 'state:', self.state[uid]
            return True

        return False
