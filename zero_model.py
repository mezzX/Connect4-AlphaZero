import torch
import torch.nn as nn
import torch.nn.functional as F

class Policy(nn.Module):

    def __init__(self, state):
        super(Policy, self).__init__()

        # 7*6 board size > 5*4
        self.conv1 = nn.Conv2d(1, 16, kernel_size=2, stride=1, bias=False)
        # 5*4 > 4*3
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, bias=False)
        # 4*3 > 384
        self.size =  4 * 3 * 32

        # 384 > 96
        self.fc_action1 = nn.Linear(self.size, self.size // 4)
        # 96 > 7
        self.fc_action2 = nn.Linear(self.size // 4, 7)

        # 384 > 64
        self.fc_value1 = nn.Linear(self.size, self.size // 6)
        # 64 > 1
        self.fc_value2 = nn.Linear(self.size // 6, 1)
        self.tanh_value = nn.Tanh()

    def forward(self, x):

        y = F.leaky_relu(self.conv1(x))
        y = F.leaky_relu(self.conv2(y))
        y = y.view(-1, self.size)

        a = F.leaky_relu(self.fc_action1(y))
        a = self.fc_action2(a)

        avail = (torch.abs(x.squeeze()) != 1).type(torch.FloatTensor)
        avail = avail.view(-1, 7)
        maxa = torch.max(a)
        exp = avail * torch.exp(a - maxa)
        prob = exp / torch.sum(exp)

        value = F.leaky_relu(self.fc_value1(y))
        value = F.leaky_relu(self.fc_value2(value))
        value = self.tanh_value(value)

        return prob.view(7, 6), value