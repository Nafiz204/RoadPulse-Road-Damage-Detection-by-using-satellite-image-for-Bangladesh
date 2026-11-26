"""
Deep Learning Architectures for RoadPulse:
1. RoadCenterline1DCNN: 1D-CNN taking sequential 6-band profile along road centerlines.
2. RoadPatchResNet18: 2D ResNet-18 adapted for 6-channel multi-spectral image chips (32x32x6).
"""
try:
    import torch
    import torch.nn as nn
    import torchvision.models as models
except ImportError:
    pass


class RoadCenterline1DCNN(nn.Module):
    """
    1D-CNN taking sequential multi-spectral profiles sampled along the road centerline.
    Input shape: (batch_size, num_bands=6, sequence_length=10)
    Output shape: (batch_size, num_classes=3)
    """
    def __init__(self, in_channels: int = 6, num_classes: int = 3):
        super().__init__()
        self.conv_block = nn.Sequential(
            nn.Conv1d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes),
        )

    def forward(self, x):
        features = self.conv_block(x)
        features = features.squeeze(-1)
        return self.classifier(features)


class RoadPatchResNet18(nn.Module):
    """
    ResNet-18 adapted for 6-channel multi-spectral Sentinel-2 image patches (32x32).
    Input shape: (batch_size, in_channels=6, height=32, width=32)
    Output shape: (batch_size, num_classes=3)
    """
    def __init__(self, in_channels: int = 6, num_classes: int = 3, pretrained: bool = True):
        super().__init__()
        base_model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT if pretrained else None)
        
        # Replace first convolution to accept 6 multi-spectral bands instead of 3 RGB channels
        orig_conv1 = base_model.conv1
        self.conv1 = nn.Conv2d(
            in_channels,
            orig_conv1.out_channels,
            kernel_size=orig_conv1.kernel_size,
            stride=orig_conv1.stride,
            padding=orig_conv1.padding,
            bias=False,
        )
        
        # Copy original RGB weights for first 3 bands, initialize remaining 3 bands
        with torch.no_grad():
            self.conv1.weight[:, :3, :, :] = orig_conv1.weight
            self.conv1.weight[:, 3:, :, :] = orig_conv1.weight.mean(dim=1, keepdim=True).repeat(1, in_channels - 3, 1, 1)

        # Replace classification head
        base_model.conv1 = self.conv1
        base_model.fc = nn.Linear(base_model.fc.in_features, num_classes)
        self.model = base_model

    def forward(self, x):
        return self.model(x)
