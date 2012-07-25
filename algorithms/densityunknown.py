import random, math

class State:
    def __init__(self, x, y, gamma):
        self.leader = None
        box_x = int(x / gamma)
        box_y = int(y / gamma)
        self.box = (box_x, box_y)
        self.phase = 0
        self.phase_round = 0
        self.conflict = False
        self.candidated = False
        self.known_leaders = set()
        self.helper = None
        self.helped = False

    def __str__(self):
        return '(leader = %s, box = %s, known_leaders = %s,' \
                'phase = %s %s, conflict = %s, candidated = %s)' \
                % (self.leader, self.box, self.known_leaders, \
                self.phase, self.phase_round, self.conflict, self.candidated)

class DensityUnknownAlgorithm():
    def __init__(self, config, e, C, d, dprim):
        self.alpha = config.alpha
        self.e = e
        self.C = C
        self.gamma = e / (math.sqrt(2) * 6)
        self.d = d
        self.dprim = dprim
        self.last_progress = 0

    def init(self, nodes, links):
        self.nodes = nodes
        self.N = len(nodes)
        self.logn = int(math.log(self.N, 2))
        self.state = {}
        for uid in self.nodes:
            self.state[uid] = State(nodes[uid].x, nodes[uid].y, self.gamma)
        source = random.choice(self.nodes.keys())
        self.state[source].leader = source
        self.active = {source}
        return {}

    def on_round_end(self, uid, messages, round_number):
        state = self.state[uid]

        #print 'state for', uid,'->', state
        if state.phase == 0:
            # leader transmission phase
            if uid == state.leader:
                res = self.leaders_transmits(uid, messages, round_number)
            else:
                res = self.nonleaders_listen(uid, messages, round_number)
            state.phase_round += 1
            if state.phase_round >= self.d**2:
                state.phase = 1
            return res
        elif state.phase == 1:
            # if not a leader
            if uid != state.leader:
                res = self.nonleaders_listen(uid, messages, round_number)
            else:
                res = False
            state.phase = 2
            state.phase_round = [0, 0, 0]
            state.conflict = False
            if state.leader == None:
                # no leader in a box
                state.helper = self.election_helper(uid)
                #print uid, 'in box', state.box, 'has helper', state.helper
            return res
        else:
            if uid in self.active:
                # leader election phase
                if state.conflict == False and state.leader == None \
                        and state.helper != None:
                    # don't have leader and no conflict so far
                    res = self.leader_election(uid, messages, round_number)
                elif state.leader == uid:
                    # uid is leader, and maybe is also a helper
                    res = self.election_help(uid, messages, round_number)
                else:
                    # not a leader, maybe conflict, maybe slave, etc.
                    res = False
            else:
                res = False

            state.phase_round[2] += 1

            if state.phase_round[2] > 2:
                state.phase_round[2] = 0
                state.phase_round[1] += 1

            if state.phase_round[1] > self.logn:
                state.phase_round[1] = 0
                state.phase_round[0] += 1

            if state.phase_round[0] >= self.dprim**2:
                state.phase = 0
                state.phase_round = 0

            return res

    def leaders_transmits(self, uid, messages, round_number):
        state = self.state[uid]
        a = int(state.phase_round / self.d)
        b = int(state.phase_round % self.d)
        if state.box[0] % self.d == a and state.box[1] % self.d == b:
            # if it's uid's time to send
            return True
        else:
            return False

    def nonleaders_listen(self, uid, messages, round_number):
        state = self.state[uid]

        if messages != [] and uid not in self.active:
            # got any message? wake up
            self.active.add(uid)
            #print uid, 'wakes up'

        for sender in messages:
            # add known leaders
            state.known_leaders.add(sender)
            #print uid, 'knows a new leader', sender

            # check if this is my leader
            if self.state[sender].box == state.box:
                state.leader = sender
                #print uid, 'knows its leader', sender

        return False

    def leader_election(self, uid, messages, round_number):
        state = self.state[uid]

        a = int(state.phase_round[0] / self.d)
        b = int(state.phase_round[0] % self.d)
        if state.box[0] % self.d == a and state.box[1] % self.d == b:
            if state.phase_round[2] == 0:
                p = (1.0 / self.N) * 2 ** state.phase_round[1]
                # transmit with pbb
                if random.random() < p:
                    #print uid, 'candidating for a leader'
                    state.candidated = True
                    return True
                else:
                    return False
            elif state.phase_round[2] == 1:
                # wait for helper
                return False
            elif state.phase_round[2] == 2:
                # if heard u? if transmitted, I'm the leader
                # transmitting if leader
                if state.candidated:
                    if state.helper in messages:
                        #print uid, 'won the leadership, celebrating'
                        state.leader = uid
                        return True
                    else:
                        #print uid, 'didn\'t win'
                        state.conflict = True
                        return False
                else:
                    return False
            elif state.phase_round[2] == 3:
                # other nodes receives the leader's and u's message
                if state.helper not in messages:
                    #print uid, 'didn\'t hear helper in K3!'
                    state.conflict = True
                else:
                    for s in messages:
                        if self.state[s].box == state.box:
                            # discovered a leader
                            #print uid, 'respects', s, 'as a leader'
                            state.leader = s
                return False
        else:
            return False

    def election_help(self, uid, messages, round_number):
        state = self.state[uid]
        if state.phase_round[2] == 0:
            # wait for leader candidate
            return False
        elif state.phase_round[2] == 1:
            # respond to the leader candidate
            if any([self.state[s].helper == uid for s in messages]):
                # if any message and uid is the helper
                #print 'helper', uid, 'helps:', messages
                state.helped = True
                return True
            else:
                state.helped = False
                return False
        elif state.phase_round[2] == 2:
            # transmit with the leader
            if state.helped:
                #print uid , 'is helping someone, so it transmits'
                return True
            else:
                return False
        elif state.phase_round[2] == 3:
            # wait for other
            return False

    def election_helper(self, uid):
        box = self.state[uid].box
        helper = None
        helper_dist = None
        for leader in self.state[uid].known_leaders:
            leader_box = self.state[leader].box
            dist = math.sqrt((box[0] - leader_box[0])**2 + \
                    (box[1] - leader_box[1])**2)
            if helper_dist == None or dist < helper_dist:
                helper = leader
                helper_dist = dist
        return helper

    def is_done(self):
        progress = len(self.active) / float(self.N)
        if progress > self.last_progress:
            self.last_progress = progress
            print 'progress:', progress
        
        return len(self.active) == self.N
