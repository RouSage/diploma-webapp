import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from flask_babel import lazy_gettext as _l
from torchvision import transforms


class CNN(nn.Module):

    def __init__(self):
        super(CNN, self).__init__()

        self.conv_layer = nn.Sequential(
            # Conv Layer block 1
            # Input: (32x32x3)
            # Output (32x32x32)
            nn.Conv2d(in_channels=3, out_channels=32,
                      kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            # Output: (32x32x64)
            nn.Conv2d(in_channels=32, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            # Output: (16x16x64)
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Conv Layer block2

            # Output: (16x16x128)
            nn.Conv2d(in_channels=64, out_channels=128,
                      kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            # Output: (16x16x128)
            nn.Conv2d(in_channels=128, out_channels=128,
                      kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            # Output: (8x8x128)
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Conv Layer block2

            # Output: (8x8x256)
            nn.Conv2d(in_channels=128, out_channels=256,
                      kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            # Output: (8x8x256)
            nn.Conv2d(in_channels=256, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            # Output: (4x4x256)
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.fc_layer = nn.Sequential(
            # 4096 = 4*4*256
            nn.Linear(in_features=4096, out_features=1024),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(in_features=1024, out_features=512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(in_features=512, out_features=10)
        )

    def forward(self, x):
        x = self.conv_layer(x)

        # Flatten
        x = x.view(x.size(0), -1)

        x = self.fc_layer(x)

        return x


data_transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

CLASSES = (_l('plane'), _l('car'), _l('bird'), _l('cat'), _l('deer'),
           _l('dog'), _l('frog'), _l('horse'), _l('ship'), _l('truck'))


def predict(model, x):
    with torch.no_grad():
        output = model(x)
        _, predicted = torch.max(output, 1)

    return predicted, F.softmax(output, dim=1).view(-1)


def prepare_image(img):
    # Resize the image to the required size
    resized_img = img.resize((32, 32))
    # And apply data transformations
    transformed_img = data_transforms(resized_img)

    return transformed_img.view(1, 3, 32, 32)


def plot_probabilities(probs, filename):
    fig, ax = plt.subplots()

    y_pos = np.arange(len(probs))
    ax.barh(y_pos, probs, color='#a02d9b')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(CLASSES)
    ax.invert_yaxis()
    ax.set_xlabel("Accuracy")
    ax.set_ylabel("Classes")

    fig.savefig(filename, format="png")
    plt.close
