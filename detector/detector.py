import torch
import torch.utils.data
import torchvision
import torchvision.datasets
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.relu = nn.ReLU()
        # 3 input image channel, 32 output channels, 3 square convolution
        self.conv1 = nn.Conv2d(3, 32, 3, stride=2)
        self.conv1_bn = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=2)
        self.conv2_bn = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, 3, stride=2)
        self.conv3_bn = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 256,3)
        self.conv4_bn = nn.BatchNorm2d(256)
        self.conv5 = nn.Conv2d(256, 512,3)
        self.conv_fc = nn.Conv2d(512,1,1, stride=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = (self.conv1_bn(self.conv1(x)))
        x = self.relu(self.conv2_bn(self.conv2(x)))
        x = self.relu(self.conv3_bn(self.conv3(x)))
        x = self.relu(self.conv4_bn(self.conv4(x)))
        x = self.relu((self.conv5(x)))
        x = self.conv_fc(x)
        x = (self.sigmoid(x)).squeeze(2).squeeze(2)
        return x

TRANSFORM_IMG_TEST = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(350),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def model_init():
    model = CNN()
    path_model = 'detector/Loss_0.7364549822540312_epoch_24.pt'
    model_weights  = torch.load(path_model)
    model.load_state_dict(model_weights)
    model.eval()
    return model
