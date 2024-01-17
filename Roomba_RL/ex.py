import random
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.autograd import Variable

# ReplayMemory クラスの定義が抜けていると仮定して以下のように追加
class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, transition):
        self.memory.append(transition)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

# Transition クラスの定義が抜けていると仮定して以下のように追加
class Transition:
    def __init__(self, state, action, next_state, reward):
        self.state = state
        self.action = action
        self.next_state = next_state
        self.reward = reward

class Brain:
    def __init__(self, num_states, num_actions):
        self.update_time = 0
        self.num_states = num_states
        self.num_actions = num_actions
        self.memory = ReplayMemory(CAPACITY)

        # メインのQネットワーク
        self.model = nn.Sequential()
        self.model.add_module('fc1', nn.Linear(self.num_states, 256))
        self.model.add_module('relu1', nn.ReLU())
        self.model.add_module('fc2', nn.Linear(256, 128))
        self.model.add_module('relu2', nn.ReLU())
        self.model.add_module('fc3', nn.Linear(128, 64))
        self.model.add_module('relu3', nn.ReLU())
        self.model.add_module('fc4', nn.Linear(64, self.num_actions))

        # ターゲットQネットワーク
        self.target_model = nn.Sequential()
        self.target_model.add_module('fc1', nn.Linear(self.num_states, 256))
        self.target_model.add_module('relu1', nn.ReLU())
        self.target_model.add_module('fc2', nn.Linear(256, 128))
        self.target_model.add_module('relu2', nn.ReLU())
        self.target_model.add_module('fc3', nn.Linear(128, 64))
        self.target_model.add_module('relu3', nn.ReLU())
        self.target_model.add_module('fc4', nn.Linear(64, self.num_actions))
        self.target_model.load_state_dict(self.model.state_dict())  # メインのQネットワークの重みをコピー

        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)

    def replay(self):
        if len(self.memory) < BATCH_SIZE:
            return

        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))
        non_final_mask = torch.ByteTensor(tuple(map(lambda s: s is not None,batch.next_state)))

        state_batch = Variable(torch.cat(batch.state))
        action_batch = Variable(torch.cat(batch.action))
        reward_batch = Variable(torch.cat(batch.reward))
        non_final_next_states = Variable(torch.cat([s for s in batch.next_state if s is not None]))

        self.model.eval()
        state_action_values = self.model(state_batch).gather(1, action_batch)

        # Target Q
        next_state_values = Variable(torch.zeros(BATCH_SIZE).type(torch.FloatTensor))
        next_state_values[non_final_mask] = self.target_model(non_final_next_states).data.max(1)[0]
        expected_state_action_values = reward_batch + GAMMA * next_state_values

        # パラメータの更新
        self.model.train()
        loss = CRITERION(state_action_values, expected_state_action_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # ターゲットネットワークの更新 (Fixed Target Q-Network)
        if self.update_time % TARGET_UPDATE == 0:
            self.target_model.load_state_dict(self.model.state_dict())

        # 記録
        self.update_time +=  1
        writer.add_scalar("loss vs. step", loss.detach().numpy(),self.update_time)
        memory_loss.append(loss.detach().numpy())
        update_count.append(self.update_time)

    # 以下省略
