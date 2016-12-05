import csv
import json
import random
from collections import defaultdict


class Bot(object):
    # The Bot class that applies the Qlearning logic to Flappy bird game
    # After every iteration (iteration = 1 game that ends with the bird dying) updates Q values
    # After every DUMPING_N iterations, dumps the Q values to the local JSON file
    def __init__(self, _upBound = 150, _botBound = 20, _learning = True, _feature = False, _exploration = False):
        self.gameCNT = 0 # Game count of current run, incremented after every death
        self.DUMPING_N = 5 # Number of iterations to dump Q values to JSON after
        self.discount = 1.0
        self.r = {0: 1, 1: -1000} # Reward function
        self.lr = 0.3

        self.last_state = "420_240_0"
        self.last_action = 0
        self.moves = []
        self.upBound = _upBound
        self.botBound = _botBound
        self.enLearn = _learning
        self.average = 0.0
        self.weights = defaultdict(float)
        self.enFeature = _feature
        self.actions = [0, 1]
        self.qvalues = {}
        self.enEpsilonGreedy = _exploration

        # if not self.enFeature:
        self.load_qvalues()
        self.validstates = set(self.qvalues.keys())

    def load_qvalues(self):
        # Load q values from a JSON file
        try:
            fil = open('qvalues.json', 'r')
        except IOError:
            return
        self.qvalues = json.load(fil)
        fil.close()

    def act(self, xdif, ydif, vel):
        # Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        def chooseMaxAction(state):
            if self.extractQ(state, 0)>= self.extractQ(state, 1):
                self.last_action = 0
                return 0
            else:
                self.last_action = 1
                return 1
        def chooseRandomAction():
            return random.randint(0, 1)

        if (self.enEpsilonGreedy):
            epilson = 0.1 * max((1 - 1.0 * self.gameCNT / 3000.0), 0)
            # epilson = 0.01
        else:
            epilson = 0.0

        if ydif >= self.upBound:
            return 0
        elif ydif <= self.botBound:
            return 1
        elif(self.enLearn):
            state = self.map_state(xdif, ydif, vel)

            self.moves.append( [self.last_state, self.last_action, state] ) # Add the experience to the history

            self.last_state = state # Update the last_state with the current state

            randomValue = random.uniform(0, 1)
            if randomValue < epilson:
                return chooseRandomAction()
            else:
                return chooseMaxAction(state)
        else:
            return 0

    def get_last_state(self):
        return self.last_state


    def update_scores(self, _score):
        #Update qvalues via iterating over experiences
        if(self.enLearn):
            history = list(reversed(self.moves))

            #Flag if the bird died in the top pipe # if ydif > 120
            high_death_flag = True if int(history[0][2].split('_')[1]) > 120 else False

            #Q-learning score updates
            t = 1
            for exp in history:
                state = exp[0]
                act = exp[1]
                res_state = exp[2]
                if t == 1 or t == 2:
                    reward = self.r[1]

                elif high_death_flag and act:
                    reward = self.r[1]
                    high_death_flag = False

                else:
                    reward = self.r[0]

                if(self.enFeature):
                    smallre = 1.0 * reward / 1000
                    Vopt_sn = max([self.extractQ(res_state, newAction) for newAction in self.actions])
                    delta = self.extractQ(state, act) - (smallre + self.discount * Vopt_sn)
                    for key, value in self.featureExtractor(state, act):
                        self.weights[key] -= self.getStepSize() * value * delta
                else:
                    if state in self.validstates and res_state in self.validstates:
                        self.qvalues[state][act] = (1 - self.lr) * (self.qvalues[state][act]) + (self.lr) * (
                            reward + (self.discount) * max(self.qvalues[res_state]))

                t += 1

            self.gameCNT += 1 #increase game count
            self.average = (self.average * (self.gameCNT - 1) + _score)/self.gameCNT
            print 'Average Score is %d, current is %d' %(self.average, _score)
            with open('result.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([_score])
            if self.enFeature:
                print self.weights
            else: self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
            self.moves = []  #clear history after updating strategies

    def map_state(self, xdif, ydif, vel):
        # Map the (xdif, ydif, vel) to the respective state, with regards to the grids
        # The state is a string, "xdif_ydif_vel"

        # X -> [-40,-30...120] U [140, 210 ... 420]
        # Y -> [-300, -290 ... 160] U [180, 240 ... 420]
        if xdif < 140:
            xdif = int(xdif) - (int(xdif) % 10)
        else:
            xdif = int(xdif) - (int(xdif) % 70)

        if ydif < 180:
            ydif = int(ydif) - (int(ydif) % 10)
        else:
            ydif = int(ydif) - (int(ydif) % 60)

        return str(int(xdif))+'_'+str(int(ydif))+'_'+str(vel)

    def dump_qvalues(self):
        # Dump the qvalues to the JSON file
        if self.gameCNT % self.DUMPING_N == 0:
            fil = open('qvalues.json', 'w')
            json.dump(self.qvalues, fil)
            fil.close()
            print('Q-values updated on local file.')

    def extractQ(self, state, action):
        if(self.enFeature):
            score = 0
            for f, v in self.featureExtractor(state, action):
                score += self.weights[f] * v
            return score
        else:
            if self.qvalues[state][action]:
                return self.qvalues[state][action]
            else:
                return 0.0

    def featureExtractor(self, state, action):
        xdif, ydif, vel = tuple(1.0 * int(word) / 1000 for word in (state.split('_')))
        result = []
        result.append((('xdif', action), xdif))
        result.append((('xdifsq2', action), xdif**2))
        result.append((('ydif', action), ydif))
        result.append((('ydifsq2', action), ydif ** 2))
        # result.append((('ydifsq3', action), ydif ** 3))
        result.append((('xydif', action), xdif*ydif))
        result.append((('vel', action), vel))
        # result.append((('velsq2', action), vel**2))
        # result.append((('ydiffvel', action), ydif*vel))
        return result

    def getStepSize(self):
        return self.lr
