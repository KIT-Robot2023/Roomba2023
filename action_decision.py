from collections import defaultdict
import numpy as np

LODING_QTABLE = 'q_tables/q_table_cal1_test2_4_2.npz'

class Q_Inference:
    def __init__(self):
        data = np.load(LODING_QTABLE)
        self.q_table = data['q_table']

    def decide_action(self, state):
        action = np.argmax(self.q_table[state])
        return action
    

class Action_decide:
    def __init__(self):
        self.q_agent = Q_Inference()
        self.num_dizitized = 5

        # 各値を離散値に変換
    def bins(self, clip_min, clip_max, num):
        return np.linspace(clip_min, clip_max, num + 1)[1:-1]

    def digitize_state(self, observation):
        distance,angle = observation
        if distance == -1 and angle == -1:
            return 25
        digitized = [
            # np.digitize(distance, bins=self.bins(0, 5.6, self.num_dizitized)),
            np.digitize(distance, bins=self.bins(0, 1, self.num_dizitized)),
            np.digitize(angle, bins=self.bins(0, 1, self.num_dizitized))
        ]

        return sum([x * (self.num_dizitized**i) for i, x in enumerate(digitized)])
    
    def ctrl(self,observation):
        state_next = self.digitize_state(observation)
        # print(state_next)
        action = self.q_agent.decide_action(state_next)  # 行動を求める
        return action